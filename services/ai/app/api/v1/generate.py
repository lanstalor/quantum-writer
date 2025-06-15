from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import httpx
from app.schemas.generation import GenerationRequest, GenerationResponse, StreamChunk
from app.services.anthropic_service import anthropic_service
from app.services.groq_service import groq_service
from app.services.openai_service import openai_service
import json
import asyncio

router = APIRouter()


async def _run_analysis(text: str) -> None:
    """Send generated text to the analysis service."""
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "http://analysis-service:8012/api/v1/analyze/characters",
                json={"text": text},
                timeout=10.0,
            )
            await client.post(
                "http://analysis-service:8012/api/v1/analyze/plot",
                json={"text": text},
                timeout=10.0,
            )
    except Exception:
        # Analysis failures should not block generation
        pass

@router.post("/generate", response_model=GenerationResponse)
async def generate_content(request: GenerationRequest, model: str = Query("groq", description="AI model to use: claude, groq, gpt")):
    """Generate story content using AI"""
    try:
        if request.stream:
            # For streaming, we'll use a different endpoint
            raise HTTPException(status_code=400, detail="Use /generate-stream for streaming responses")
        
        if model == "groq":
            content = await groq_service.generate_content(
                prompt=request.prompt,
                context=request.context,
                system_prompt=request.system_prompt
            )
            tokens_used = groq_service.estimate_tokens(content)
        elif model == "gpt" or model == "openai":
            content = await openai_service.generate_content(
                prompt=request.prompt,
                context=request.context,
                system_prompt=request.system_prompt
            )
            tokens_used = openai_service.estimate_tokens(content)
        else:  # default to claude
            content = await anthropic_service.generate_content(
                prompt=request.prompt,
                context=request.context,
                system_prompt=request.system_prompt
            )
            tokens_used = anthropic_service.estimate_tokens(content)

        await _run_analysis(content)

        return GenerationResponse(
            content=content,
            tokens_used=tokens_used
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.post("/generate-stream")
async def generate_content_stream(request: GenerationRequest):
    """Generate story content using AI with streaming"""
    try:
        async def generate():
            accumulated_content = ""
            async for chunk in anthropic_service.generate_content_stream(
                prompt=request.prompt,
                context=request.context,
                system_prompt=request.system_prompt
            ):
                accumulated_content += chunk
                chunk_data = StreamChunk(content=chunk, done=False)
                yield f"data: {chunk_data.model_dump_json()}\n\n"
                
                # Small delay to prevent overwhelming the client
                await asyncio.sleep(0.01)
            
            # Send final chunk
            final_chunk = StreamChunk(content="", done=True)
            yield f"data: {final_chunk.model_dump_json()}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Streaming generation failed: {str(e)}")

@router.post("/continue-story", response_model=GenerationResponse)
async def continue_story(request: GenerationRequest, model: str = Query("groq", description="AI model to use: claude, groq, gpt")):
    """Continue an existing story with AI generation"""
    try:
        # Add specific system prompt for story continuation
        story_system_prompt = """You are a creative writing assistant helping to continue an existing story. 
        Maintain consistency with the existing narrative, characters, and writing style. 
        Generate engaging content that flows naturally from the previous chapters."""
        
        if request.system_prompt:
            story_system_prompt = f"{story_system_prompt}\n\nAdditional instructions: {request.system_prompt}"
        
        if model == "groq":
            content = await groq_service.generate_content(
                prompt=request.prompt,
                context=request.context,
                system_prompt=story_system_prompt
            )
            tokens_used = groq_service.estimate_tokens(content)
        elif model == "gpt" or model == "openai":
            content = await openai_service.generate_content(
                prompt=request.prompt,
                context=request.context,
                system_prompt=story_system_prompt
            )
            tokens_used = openai_service.estimate_tokens(content)
        else:  # default to claude
            content = await anthropic_service.generate_content(
                prompt=request.prompt,
                context=request.context,
                system_prompt=story_system_prompt
            )
            tokens_used = anthropic_service.estimate_tokens(content)

        await _run_analysis(content)

        return GenerationResponse(
            content=content,
            tokens_used=tokens_used
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Story continuation failed: {str(e)}")