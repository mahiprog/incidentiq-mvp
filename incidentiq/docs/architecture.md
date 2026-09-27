# IncidentIQ Architecture

## Core loop

Current incident -> investigation -> Hindsight recall -> recommendation -> resolution -> Hindsight retain.

## Why Hindsight?

Hindsight is the persistent memory layer. The application retains incident experiences and recalls relevant historical memories during later investigations.

## Components

- React frontend: incident dashboard
- FastAPI backend: REST API
- Incident agent: orchestration and reasoning
- Hindsight: persistent memory
- Tools: incident, log and metric adapters
