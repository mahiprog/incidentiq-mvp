# IncidentIQ

An autonomous incident-response MVP that gives an engineering team persistent organizational memory.

## Core idea

IncidentIQ remembers production incidents, recalls similar historical experiences during new incidents, and stores the outcome of new resolutions.

## Stack

- Python + FastAPI
- React + Vite
- Hindsight memory
- Sample incident data

## 1. Backend

Create a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure Hindsight.

Start:

```bash
uvicorn backend.main:app --reload --port 8000
```

## 2. Hindsight

The official Hindsight Python client is `hindsight-client`.

For a local Hindsight API, run Hindsight separately on port 8888 and set:

```env
HINDSIGHT_API_URL=http://localhost:8888
```

For Hindsight Cloud, set its API URL and API key.

## 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal.

## 4. Demo flow

1. Investigate a payment incident.
2. Show similar historical incidents.
3. Retain a resolution using Hindsight.
4. Investigate a similar incident.
5. Show recalled Hindsight memories.
6. Resolve and retain the new outcome.

## Important

The current investigator intentionally uses deterministic rules for the MVP so the demo works without depending on a second LLM service. Hindsight remains the persistent memory layer. You can add an LLM reasoning layer after the memory loop is working.
