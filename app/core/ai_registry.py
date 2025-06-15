from ..domain.ai.adapters import ClaudeAdapter, GPT4Adapter, GroqAdapter, BaseModelAdapter

registry: dict[str, BaseModelAdapter] = {
    "claude": ClaudeAdapter(),
    "gpt4": GPT4Adapter(),
    "groq": GroqAdapter(),
}
