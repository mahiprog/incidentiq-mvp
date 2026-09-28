import pytest
from backend.tools.detector import detect_incident
from backend.tools.metrics import get_metrics
from backend.tools.logs import get_recent_logs
from backend.agent.investigator import build_investigation


def test_detect_incident_payment_api():
    result = detect_incident("payment-api")
    assert result is not None
    assert result["service"] == "payment-api"
    assert result["error_rate"] >= 10
    assert result["incident_id"].startswith("INC-AUTO-")


def test_detect_incident_healthy_service():
    result = detect_incident("healthy-service")
    assert result is None


def test_get_metrics_payment_api():
    metrics = get_metrics("payment-api")
    assert metrics["service"] == "payment-api"
    assert "error_rate" in metrics
    assert "latency_ms" in metrics
    assert "availability" in metrics


def test_get_logs_payment_api():
    logs = get_recent_logs("payment-api")
    assert isinstance(logs, list)
    assert len(logs) > 0


def test_build_investigation_with_memories():
    incident = {
        "service": "payment-api",
        "error": "502 Bad Gateway",
        "error_rate": 18,
        "recent_change": "payment-config-v4",
    }
    memories = [{"text": "Rolled back config, error rate dropped."}]
    result = build_investigation(incident, memories, [])
    assert result["memory_count"] == 1
    assert len(result["memory_insights"]) == 1
    assert "recalled experience" in result["recommendation"].lower()


def test_build_investigation_no_memories():
    incident = {
        "service": "payment-api",
        "error": "502 Bad Gateway",
        "error_rate": 18,
        "recent_change": "payment-config-v4",
    }
    result = build_investigation(incident, [], [])
    assert result["memory_count"] == 0
    assert "Inspect" in result["recommendation"]
