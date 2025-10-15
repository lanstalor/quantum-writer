from __future__ import annotations

from pydantic_settings import BaseSettings

from typing import Dict, List, Optional
import asyncio
import hashlib
import logging
import uuid

try:
    from qdrant_client import AsyncQdrantClient
    from qdrant_client.http import models as qmodels
except ImportError:  # pragma: no cover - optional dependency during tests
    AsyncQdrantClient = None  # type: ignore
    qmodels = None  # type: ignore


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Settings(BaseSettings):
    SERVICE_NAME: str = "context-service"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/quantum_writer"
    MAX_CONTEXT_TOKENS: int = 4096
    VECTOR_DB_URL: Optional[str] = "http://localhost:6333"
    QDRANT_COLLECTION: str = "story_context"
    EMBEDDING_SIZE: int = 8

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()


_fallback_segments: Dict[str, List[Dict[str, str]]] = {}
_fallback_lock = asyncio.Lock()

if AsyncQdrantClient is not None and settings.VECTOR_DB_URL:
    qdrant_client: Optional[AsyncQdrantClient] = AsyncQdrantClient(url=settings.VECTOR_DB_URL)
else:  # pragma: no cover - exercised when dependency missing
    qdrant_client = None


async def _disable_qdrant(reason: str, exc: Optional[Exception] = None) -> None:
    """Tear down the Qdrant client and fall back to the in-memory store."""
    global qdrant_client
    client = qdrant_client
    if client is not None:
        try:
            await client.close()  # type: ignore[func-returns-value]
        except Exception:  # pragma: no cover - best effort cleanup
            pass
    qdrant_client = None
    if exc is not None:
        logger.warning("Qdrant disabled (%s): %s", reason, exc)
    else:
        logger.warning("Qdrant disabled (%s)", reason)


async def _store_fallback_segment(story_id: str, text: str, point_id: Optional[str] = None) -> str:
    point_id = point_id or str(uuid.uuid4())
    async with _fallback_lock:
        segments = _fallback_segments.setdefault(story_id, [])
        segments.append({"id": point_id, "text": text})
    return point_id


async def _search_fallback_segments(story_id: str, query: str, limit: int) -> List[Dict[str, float | str]]:
    lowered = query.lower()
    async with _fallback_lock:
        segments = list(_fallback_segments.get(story_id, []))
    scored = [
        {"text": segment["text"], "score": 1.0 if lowered in segment["text"].lower() else 0.0}
        for segment in segments
    ]
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:limit]


async def init_vector_store() -> None:
    """Ensure the Qdrant collection exists or fall back to the in-memory store."""
    client = qdrant_client
    if client is None or not settings.VECTOR_DB_URL or qmodels is None:
        logger.info("Vector store initialisation skipped; using in-memory fallback.")
        return

    try:
        await client.get_collection(settings.QDRANT_COLLECTION)
    except Exception as exc:
        logger.debug("Qdrant collection lookup failed: %s", exc)
        try:
            await client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=qmodels.VectorParams(
                    size=settings.EMBEDDING_SIZE,
                    distance=qmodels.Distance.COSINE,
                ),
            )
        except Exception as create_exc:
            await _disable_qdrant("initialisation failed", create_exc)


def embed_text(text: str) -> List[float]:
    """Deterministically embed text into a fixed-size vector."""
    digest = hashlib.sha256(text.encode()).digest()
    vec = [
        int.from_bytes(digest[i * 4 : (i + 1) * 4], "little") / 2**32
        for i in range(settings.EMBEDDING_SIZE)
    ]
    return vec


async def store_context_segment(story_id: str, text: str) -> str:
    """Store a single context segment and return its identifier."""
    point_id = str(uuid.uuid4())
    client = qdrant_client

    if client is None or qmodels is None:
        return await _store_fallback_segment(story_id, text, point_id)

    vector = embed_text(text)
    try:
        await client.upsert(
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
    except Exception as exc:
        await _disable_qdrant("upsert failed", exc)
        return await _store_fallback_segment(story_id, text, point_id)


async def search_story_segments(story_id: str, query: str, limit: int = 5):
    """Return the most similar segments for the given query."""
    client = qdrant_client

    if client is None or qmodels is None:
        return await _search_fallback_segments(story_id, query, limit)

    vector = embed_text(query)
    flt = qmodels.Filter(
        must=[qmodels.FieldCondition(key="story_id", match=qmodels.MatchValue(value=story_id))]
    )
    try:
        results = await client.search(
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
    except Exception as exc:
        await _disable_qdrant("search failed", exc)
        return await _search_fallback_segments(story_id, query, limit)

