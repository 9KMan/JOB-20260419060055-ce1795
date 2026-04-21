from supabase import create_client, Client
from app.core.config import settings
from typing import Optional


class SupabaseService:
    def __init__(self):
        self._client: Optional[Client] = None

    def get_client(self) -> Client:
        if self._client is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                raise ValueError("Supabase credentials not configured")
            self._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return self._client

    def create_client(url: str, key: str) -> Client:
        return create_client(url, key)


supabase_service = SupabaseService()


def get_supabase() -> Client:
    return supabase_service.get_client()
