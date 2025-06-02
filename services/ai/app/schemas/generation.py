from pydantic import BaseModel, Field
from typing import Optional

class GenerationRequest(BaseModel):
    prompt: str = Field(..., description="The prompt for content generation")
    context: Optional[str] = Field(default="", description="Previous story context")
    system_prompt: Optional[str] = Field(default="", description="System instructions for the AI")
    max_tokens: Optional[int] = Field(default=4000, ge=1, le=8000, description="Maximum tokens to generate")
    stream: Optional[bool] = Field(default=False, description="Whether to stream the response")

class GenerationResponse(BaseModel):
    content: str = Field(..., description="Generated content")
    tokens_used: Optional[int] = Field(default=None, description="Estimated tokens used")

class StreamChunk(BaseModel):
    content: str = Field(..., description="Chunk of generated content")
    done: bool = Field(default=False, description="Whether this is the final chunk")