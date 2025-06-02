import os
from typing import Dict, Any, AsyncGenerator
from groq import Groq
import asyncio

class GroqService:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.client = Groq(api_key=self.api_key)
        self.max_context_length = 128000  # Llama 3.1 8B context window
        
    async def generate_content(self, prompt: str, context: str = "", system_prompt: str = "", model: str = "llama-3.1-8b-instant") -> str:
        """Generate content using Groq API"""
        try:
            # Combine context and prompt
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Default system prompt if none provided
            if not system_prompt:
                system_prompt = "You are a creative writing assistant helping to generate engaging story content. Write compelling, original fiction."
            
            # Groq API is synchronous, so we run it in an executor
            def _generate():
                completion = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ],
                    max_tokens=4000,
                    temperature=0.7,
                    top_p=0.9
                )
                return completion.choices[0].message.content
            
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, _generate)
            
        except Exception as e:
            print(f"Error generating content with Groq: {e}")
            raise e
    
    async def generate_content_stream(self, prompt: str, context: str = "", system_prompt: str = "", model: str = "llama-3.1-8b-instant") -> AsyncGenerator[str, None]:
        """Generate content using Groq API with streaming"""
        try:
            # Combine context and prompt
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Default system prompt if none provided
            if not system_prompt:
                system_prompt = "You are a creative writing assistant helping to generate engaging story content. Write compelling, original fiction."
            
            def _generate_stream():
                return self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ],
                    max_tokens=4000,
                    temperature=0.7,
                    top_p=0.9,
                    stream=True
                )
            
            loop = asyncio.get_event_loop()
            stream = await loop.run_in_executor(None, _generate_stream)
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"Error generating streaming content with Groq: {e}")
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
groq_service = GroqService()