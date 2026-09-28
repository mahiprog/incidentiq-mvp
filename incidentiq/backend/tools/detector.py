from .metrics import get_metrics
from .logs import get_recent_logs
import uuid

THRESHOLDS = {
    "error_rate": 10.0,
    "latency_ms": 700,
    "availability": 99.5,
}

def detect_incident(service: str) -> dict | None:
    metrics = get_metrics(service)
    logs = get_recent_logs(service)

    problems = []
    error = ""

    if metrics["error_rate"] >= THRESHOLDS["error_rate"]:
        problems.append(f"High error rate: {metrics['error_rate']}%")
        error = "502 Bad Gateway" if "502" in " ".join(logs) else "High error rate"

    if metrics["latency_ms"] >= THRESHOLDS["latency_ms"]:
        problems.append(f"High latency: {metrics['latency_ms']}ms")
        if not error:
            error = "Latency threshold exceeded"

    if metrics["availability"] < THRESHOLDS["availability"]:
        problems.append(f"Low availability: {metrics['availability']}%")
        if not error:
            error = "Availability degraded"

    if not problems:
        return None

    return {
        "incident_id": f"INC-AUTO-{uuid.uuid4().hex[:6].upper()}",
        "service": service,
        "severity": "critical" if metrics["error_rate"] >= 15 else "high",
        "error_rate": metrics["error_rate"],
        "error": error,
        "recent_change": metrics.get("recent_change", ""),
        "description": " | ".join(problems),
        "metrics": metrics,
        "logs": logs,
    }
