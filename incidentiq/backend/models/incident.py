from pydantic import BaseModel

class Incident(BaseModel):
    incident_id: str
    service: str
    severity: str
    error_rate: float
    error: str
    recent_change: str = ""
    description: str = ""
