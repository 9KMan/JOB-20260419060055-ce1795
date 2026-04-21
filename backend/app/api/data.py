from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import create_client

from app.core.config import settings
from app.api.auth import get_current_user

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/items")
async def list_items(
    table: str = "items",
    current_user: str = Depends(get_current_user),
):
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase not configured",
        )

    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    try:
        response = supabase.table(table).select("*").execute()
        return {"items": response.data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/items")
async def create_item(
    table: str = "items",
    data: dict = {},
    current_user: str = Depends(get_current_user),
):
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase not configured",
        )

    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    try:
        response = supabase.table(table).insert(data).execute()
        return {"item": response.data[0] if response.data else None}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api"}
