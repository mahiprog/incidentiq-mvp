import os
from functools import lru_cache
from hindsight_client import Hindsight

BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "incidentiq")

@lru_cache(maxsize=1)
def get_client():
    base_url = os.getenv("HINDSIGHT_API_URL", "http://localhost:8888")
    api_key = os.getenv("HINDSIGHT_API_KEY") or None
    return Hindsight(base_url=base_url, api_key=api_key)

def get_bank_id() -> str:
    return BANK_ID
