from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from backend.agent.incident_agent import investigate_incident
from backend.hindsight.retain import retain_incident
from backend.hindsight.recall import recall_incidents
from backend.tools.incidents import (
    seed_incidents,
    get_incident,
    list_incidents,
)

app = FastAPI(
    title="IncidentIQ API",
    version="0.1.0",
)

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------

class IncidentRequest(BaseModel):
    incident_id: str
    service: str
    severity: str
    error_rate: float
    error: str
    recent_change: str = ""
    description: str = ""


class ResolutionRequest(BaseModel):
    incident_id: str
    action: str
    result: str
    service: str = ""
    error: str = ""


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "incidentiq",
    }


# ---------------------------------------------------------
# Seed Sample Incidents
# ---------------------------------------------------------

@app.post("/seed")
def seed():
    return {
        "incidents": seed_incidents()
    }


# ---------------------------------------------------------
# List Incidents
# ---------------------------------------------------------

@app.get("/incidents")
def incidents():
    return list_incidents()


# ---------------------------------------------------------
# Get Single Incident
# ---------------------------------------------------------

@app.get("/incidents/{incident_id}")
def incident(incident_id: str):
    item = get_incident(incident_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return item


# ---------------------------------------------------------
# AI Incident Investigation
# ---------------------------------------------------------

@app.post("/investigate")
def investigate(req: IncidentRequest):
    incident_data = req.model_dump()

    result = investigate_incident(
        incident_data
    )

    return result


# ---------------------------------------------------------
# Resolve Incident + Store Memory
# ---------------------------------------------------------

@app.post("/incidents/{incident_id}/resolve")
def resolve(
    incident_id: str,
    req: ResolutionRequest,
):
    if incident_id != req.incident_id:
        raise HTTPException(
            status_code=400,
            detail="incident_id mismatch",
        )

    payload = {
        "incident_id": incident_id,
        "action": req.action,
        "result": req.result,
    }

    # enrich with service/error from stored incident for better recall matching
    stored = get_incident(incident_id)
    if stored:
        payload["service"] = stored.get("service", "")
        payload["error"] = stored.get("error", "")
    else:
        payload["service"] = getattr(req, "service", "")
        payload["error"] = getattr(req, "error", "")

    try:
        memory_result = retain_incident(
            payload
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Hindsight retain failed: {exc}",
        )

    return {
        "status": "stored",
        "memory": memory_result,
    }


# ---------------------------------------------------------
# Hindsight Memory Recall
# ---------------------------------------------------------

@app.get("/memory/recall")
def recall(q: str):
    try:
        results = recall_incidents(q)

        return {
            "query": q,
            "results": results,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Hindsight recall failed: {exc}",
        )