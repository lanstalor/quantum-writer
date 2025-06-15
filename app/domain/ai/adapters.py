import asyncio
from typing import AsyncGenerator


class BaseModelAdapter:
    name: str

    async def generate(self, prompt: str) -> AsyncGenerator[str, None]:
        raise NotImplementedError


class ClaudeAdapter(BaseModelAdapter):
    name = "claude"

    async def generate(self, prompt: str) -> AsyncGenerator[str, None]:
        for token in prompt.split():
            await asyncio.sleep(1)
            yield token


class GPT4Adapter(BaseModelAdapter):
    name = "gpt4"

    async def generate(self, prompt: str) -> AsyncGenerator[str, None]:
        for token in prompt.split():
            await asyncio.sleep(1)
            yield token


class GroqAdapter(BaseModelAdapter):
    name = "groq"

    async def generate(self, prompt: str) -> AsyncGenerator[str, None]:
        for token in prompt.split():
            await asyncio.sleep(1)
            yield token
