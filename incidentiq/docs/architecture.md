# IncidentIQ Architecture

## Overview

IncidentIQ is an autonomous incident-response agent that uses Hindsight persistent memory to recall past incidents, learn from successful resolutions, and recommend context-aware actions for future incidents.

## Pipeline

```
LIVE APPLICATION
      │
      ├── Metrics (error_rate, latency_ms, availability)
      └── Logs (service log stream)
            │
            ▼
    Detection Engine
    (threshold-based anomaly detection)
            │
            ▼
       🚨 INCIDENT
    (auto-created with severity, service, error)
            │
            ▼
     Incident Agent
            │
            ├── Hindsight RECALL
            │   (semantic search over past resolutions)
            │
            ├── Local similarity matching
            │   (service + error pattern scoring)
            │
            └── Investigation builder
                (evidence, hypotheses, recommendation)
                    │
                    ▼
           AI Recommendation
                    │
                    ▼
          Human Approval (UI)
                    │
                    ▼
          Resolve Incident
                    │
                    ▼
          Hindsight RETAIN
          (stores resolution for future recall)
```

## Components

### Backend (Python / FastAPI)
- `backend/main.py` — REST API, all endpoints
- `backend/agent/incident_agent.py` — orchestrates detection → recall → investigation
- `backend/agent/investigator.py` — builds evidence, hypotheses, recommendation
- `backend/agent/prompts.py` — constructs LLM-ready prompt with recalled memories
- `backend/hindsight/recall.py` — queries Hindsight memory bank
- `backend/hindsight/retain.py` — stores resolution in Hindsight memory bank
- `backend/tools/detector.py` — threshold-based incident detection from metrics + logs
- `backend/tools/metrics.py` — simulated live metrics per service
- `backend/tools/logs.py` — simulated log stream per service

### Frontend (React / Vite)
- `frontend/src/main.jsx` — full pipeline UI: detect → investigate → approve → resolve

### Memory (Hindsight)
- Bank ID: `incidentiq`
- Retain: stores incident ID, service, error, action, result
- Recall: semantic search by service + error + description query

### Infrastructure
- `Dockerfile` — containerized backend
- `docker-compose.yml` — full stack orchestration
- `.github/workflows/ci.yml` — CI pipeline (lint + test + build)

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/incidents` | List all incidents |
| GET | `/incidents/{id}` | Get single incident |
| POST | `/investigate` | Run AI investigation |
| POST | `/incidents/{id}/resolve` | Resolve and retain in Hindsight |
| GET | `/monitor/{service}` | Detect incident from live metrics |
| GET | `/monitor/{service}/investigate` | Full pipeline in one call |
| GET | `/memory/recall?q=` | Query Hindsight memory bank |

## Why Hindsight?

Hindsight provides the persistent organizational memory layer. Without it, every incident is investigated in isolation. With it, the agent recalls what worked before and surfaces that experience directly in the recommendation — making the system smarter with every resolved incident.
