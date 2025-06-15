import os
import random
from typing import Sequence

try:
    import openai
except Exception:  # pragma: no cover
    openai = None


async def embed(text: str) -> Sequence[float]:
    if openai and os.getenv("OPENAI_API_KEY"):
        resp = await openai.Embedding.acreate(model="text-embedding-ada-002", input=text)
        return resp["data"][0]["embedding"]
    # fallback deterministic random for tests
    random.seed(text)
    return [random.random() for _ in range(768)]
