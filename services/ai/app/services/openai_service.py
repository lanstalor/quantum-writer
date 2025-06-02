import os
import openai
from typing import Dict, Any, AsyncGenerator
import asyncio

class OpenAIService:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.AsyncOpenAI(api_key=self.api_key)
        self.max_context_length = 128000  # GPT-4o-mini context window
        
    async def generate_content(self, prompt: str, context: str = "", system_prompt: str = "", model: str = "gpt-4o-mini") -> str:
        """Generate content using OpenAI API"""
        try:
            # Combine context and prompt
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Default system prompt if none provided
            if not system_prompt:
                system_prompt = "You are a creative writing assistant helping to generate engaging story content. Write compelling, original fiction with vivid descriptions and strong character development."
            
            completion = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=4000,
                temperature=0.8,
                top_p=0.9
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating content with OpenAI: {e}")
            raise e
    
    async def generate_content_stream(self, prompt: str, context: str = "", system_prompt: str = "", model: str = "gpt-4o-mini") -> AsyncGenerator[str, None]:
        """Generate content using OpenAI API with streaming"""
        try:
            # Combine context and prompt
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Default system prompt if none provided
            if not system_prompt:
                system_prompt = "You are a creative writing assistant helping to generate engaging story content. Write compelling, original fiction with vivid descriptions and strong character development."
            
            stream = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=4000,
                temperature=0.8,
                top_p=0.9,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"Error generating streaming content with OpenAI: {e}")
            raise e
    
    def estimate_tokens(self, text: str) -> int:
        """Rough estimation of token count (4 chars = 1 token approximately)"""
        return len(text) // 4
    
    def truncate_context(self, context: str, max_tokens: int = 120000) -> str:
        """Truncate context to fit within token limits"""
        estimated_tokens = self.estimate_tokens(context)
        if estimated_tokens <= max_tokens:
            return context
        
        # Truncate from the beginning, keeping the most recent context
        ratio = max_tokens / estimated_tokens
        truncate_point = int(len(context) * (1 - ratio))
        return context[truncate_point:]

# Global instance
openai_service = OpenAIService()