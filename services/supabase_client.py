import os
from supabase_py import create_client, Client
from dotenv import load_dotenv
import sys

load_dotenv()

class SupabaseClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance

    def _initialize(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("Supabase credentials not found in .env")
            
        try:
            self.client = create_client(supabase_url=url, supabase_key=key)
            # Test connection
            self.client.auth.get_session()
        except Exception as e:
            print(f"Supabase initialization error: {str(e)}", file=sys.stderr)
            raise

    def get_client(self) -> Client:
        if self.client is None:
            self._initialize()
        return self.client

def get_supabase():
    try:
        return SupabaseClient().get_client()
    except Exception as e:
        print(f"Failed to get Supabase client: {str(e)}", file=sys.stderr)
        raise
