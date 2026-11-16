
from supabase import Client, create_client

from app.core.config import settings


class SupabaseConnection:

    def __init__(self):
        self._client = None

    def connect(self) -> Client:

        if self._client is None:

            if not settings.SUPABASE_URL:
                raise ValueError("SUPABASE_URL is missing")

            if not settings.SUPABASE_KEY:
                raise ValueError("SUPABASE_KEY is missing")

            self._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )

        return self._client


supabase_connection = SupabaseConnection()
