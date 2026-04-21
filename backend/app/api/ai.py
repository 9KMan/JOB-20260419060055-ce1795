from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.core.config import settings
from app.models.schemas import UserResponse
from app.services.ai import get_ai_service, AIService
from app.api.auth import get_current_user

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate")
async def generate_content(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1000,
    temperature: float = 0.7,
    current_user: str = Depends(get_current_user),
    ai_service: AIService = Depends(get_ai_service),
):
    try:
        result = await ai_service.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI generation failed: {str(e)}",
        )


@router.post("/chat")
async def chat(
    messages: List[dict],
    max_tokens: int = 1000,
    temperature: float = 0.7,
    current_user: str = Depends(get_current_user),
):
    try:
        from openai import ChatCompletion

        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", ""),
            })

        response = await ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=formatted_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI chat failed: {str(e)}",
        )
