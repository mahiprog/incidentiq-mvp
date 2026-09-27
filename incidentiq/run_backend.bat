@echo off
call .venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000
