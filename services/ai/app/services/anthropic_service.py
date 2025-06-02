import anthropic
import os
from typing import Dict, Any, AsyncGenerator
from app.core import settings

class AnthropicService:
    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.max_context_length = 100000  # Claude's context window size
        
    async def generate_content(self, prompt: str, context: str = "", system_prompt: str = "") -> str:
        """Generate content using Claude API"""
        try:
            # Combine context and prompt
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Default system prompt if none provided
            if not system_prompt:
                system_prompt = "You are a creative writing assistant helping to generate engaging story content."
            
            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                system=system_prompt,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error generating content: {e}")
            raise e
    
    async def generate_content_stream(self, prompt: str, context: str = "", system_prompt: str = "") -> AsyncGenerator[str, None]:
        """Generate content using Claude API with streaming"""
        try:
            # Combine context and prompt
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Default system prompt if none provided
            if not system_prompt:
                system_prompt = "You are a creative writing assistant helping to generate engaging story content."
            
            with self.client.messages.stream(
                model="claude-3-opus-20240229",
                system=system_prompt,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            print(f"Error generating streaming content: {e}")
            raise e
    
    def estimate_tokens(self, text: str) -> int:
        """Rough estimation of token count (4 chars = 1 token approximately)"""
        return len(text) // 4
    
    def truncate_context(self, context: str, max_tokens: int = 90000) -> str:
        """Truncate context to fit within token limits"""
        estimated_tokens = self.estimate_tokens(context)
        if estimated_tokens <= max_tokens:
            return context
        
        # Truncate from the beginning, keeping the most recent context
        ratio = max_tokens / estimated_tokens
        truncate_point = int(len(context) * (1 - ratio))
        return context[truncate_point:]

# Global instance
anthropic_service = AnthropicService()