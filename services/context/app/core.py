from pydantic_settings import BaseSettings

from typing import List
import hashlib
import uuid

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models as qmodels


class Settings(BaseSettings):
    SERVICE_NAME: str = "context-service"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/quantum_writer"
    MAX_CONTEXT_TOKENS: int = 4096
    VECTOR_DB_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "story_context"
    EMBEDDING_SIZE: int = 8

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Global Qdrant client
qdrant_client = AsyncQdrantClient(url=settings.VECTOR_DB_URL)


async def init_vector_store() -> None:
    """Ensure the Qdrant collection exists."""
    try:
        await qdrant_client.get_collection(settings.QDRANT_COLLECTION)
    except Exception:
        await qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=qmodels.VectorParams(
                size=settings.EMBEDDING_SIZE,
                distance=qmodels.Distance.COSINE,
            ),
        )


def embed_text(text: str) -> List[float]:
    """Deterministically embed text into a fixed-size vector."""
    digest = hashlib.sha256(text.encode()).digest()
    vec = [
        int.from_bytes(digest[i * 4 : (i + 1) * 4], "little") / 2**32
        for i in range(settings.EMBEDDING_SIZE)
    ]
    return vec


async def store_context_segment(story_id: str, text: str) -> str:
    """Store a single context segment in Qdrant and return its id."""
    vector = embed_text(text)
    point_id = str(uuid.uuid4())
    await qdrant_client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        wait=True,
        points=[
            qmodels.PointStruct(
                id=point_id,
                vector=vector,
                payload={"story_id": story_id, "text": text},
            )
        ],
    )
    return point_id


async def search_story_segments(story_id: str, query: str, limit: int = 5):
    """Return the most similar segments for the given query."""
    vector = embed_text(query)
    flt = qmodels.Filter(
        must=[qmodels.FieldCondition(key="story_id", match=qmodels.MatchValue(value=story_id))]
    )
    results = await qdrant_client.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=vector,
        query_filter=flt,
        limit=limit,
        with_payload=True,
    )
    return [
        {"text": r.payload.get("text", ""), "score": r.score}
        for r in results
    ]

