# ai_interface.py
import anthropic
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

class AIInterface:
    def __init__(self, api_key: str = None):
        # Use API key from parameter, env variable, or None
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.max_context_length = 100000  # Claude's context window size # Claude's context window size
        
    def generate_content(self, prompt: str, context: str, system_prompt: str) -> str:
        """Generate content using Claude API"""
        try:
            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                system=system_prompt,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": context + "\n\n" + prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""
