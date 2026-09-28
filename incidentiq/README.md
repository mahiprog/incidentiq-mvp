# IncidentIQ

An autonomous incident-response agent that uses [Hindsight](https://hindsight.vectorize.io/) persistent memory to recall past incidents, learn from successful resolutions, and recommend context-aware actions for future incidents.

## How it works

```
Live Metrics + Logs
        ↓
Detection Engine  →  🚨 Incident Created
        ↓
Incident Agent
        ↓
Hindsight RECALL  →  Historical Experience
        ↓
AI Recommendation
        ↓
Human Approval
        ↓
Resolve Incident
        ↓
Hindsight RETAIN  →  Memory stored for future incidents
```

Every resolved incident makes the system smarter. The next similar incident gets the benefit of everything that worked before.

## Stack

| Layer | Technology |
|-------|-----------|
| Backend API | Python 3.11, FastAPI |
| Frontend | React 19, Vite |
| Memory | Hindsight (vectorize.io) |
| Containerization | Docker, Docker Compose |
| CI | GitHub Actions |
| Schema | PostgreSQL-compatible SQL |

## Quick Start

### 1. Backend

```bash
cd incidentiq
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # fill in Hindsight credentials
uvicorn backend.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd incidentiq/frontend
npm install
npm run dev
```

Open `http://localhost:5173`

### 3. Docker (full stack)

```bash
cd incidentiq
docker-compose up --build
```

## Environment Variables

```env
HINDSIGHT_API_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=your_api_key_here
HINDSIGHT_BANK_ID=incidentiq
```

Get your API key at [ui.hindsight.vectorize.io](https://ui.hindsight.vectorize.io).

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/incidents` | List incidents |
| POST | `/investigate` | AI investigation |
| POST | `/incidents/{id}/resolve` | Resolve + retain in Hindsight |
| GET | `/monitor/{service}` | Auto-detect from live metrics |
| GET | `/monitor/{service}/investigate` | Full pipeline in one call |
| GET | `/memory/recall?q=` | Query Hindsight memory |

## Demo Flow

1. Open the dashboard at `http://localhost:5173`
2. Click **▶ Run Detection** — metrics and logs are scanned, incident auto-created
3. Investigation runs automatically — Hindsight recalled memories appear
4. Click **✓ Approve & Execute**
5. Click **Resolve & Remember** — resolution stored in Hindsight
6. Run detection again — `1 historical memories` confirms the learning loop

## Tests

```bash
cd incidentiq
pip install pytest
pytest tests/ -v
```

## Project Structure

```
incidentiq/
├── backend/
│   ├── agent/          # Investigation orchestration
│   ├── hindsight/      # Recall + retain
│   ├── models/         # Pydantic models
│   ├── tools/          # Metrics, logs, detector
│   └── main.py         # FastAPI app
├── frontend/           # React + Vite
├── data/
│   ├── sample_incidents/
│   └── schema.sql      # Reference DB schema
├── docs/               # Architecture + demo guide
├── tests/              # Pytest suite
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/  # CI pipeline
```

## Built with Hindsight

This project was built for the Hindsight hackathon. Hindsight is the persistent memory layer — without it, every incident is investigated in isolation. With it, the agent recalls what worked before and surfaces that experience directly in the recommendation.

- [Hindsight Documentation](https://hindsight.vectorize.io/)
- [Hindsight Cloud](https://ui.hindsight.vectorize.io)
- [GitHub](https://github.com/vectorize-io/hindsight)
