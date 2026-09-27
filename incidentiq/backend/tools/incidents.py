from copy import deepcopy

INCIDENTS = [
    {
        "incident_id": "INC-004",
        "service": "payment-api",
        "severity": "critical",
        "error_rate": 18,
        "error": "502 Bad Gateway",
        "recent_change": "payment-config-v4",
        "description": "Payment failures increased shortly after a configuration deployment.",
        "root_cause": "Invalid payment configuration",
        "resolution": "Rollback configuration",
        "result": "Error rate reduced from 18% to 1%",
    },
    {
        "incident_id": "INC-001",
        "service": "payment-api",
        "severity": "critical",
        "error_rate": 18,
        "error": "502 Bad Gateway",
        "recent_change": "payment-config-v2",
        "description": "Payment requests started failing shortly after a configuration deployment.",
        "root_cause": "Invalid payment configuration",
        "resolution": "Rollback configuration",
        "result": "Error rate reduced from 18% to 1%",
    },
    {
        "incident_id": "INC-002",
        "service": "checkout-api",
        "severity": "high",
        "error_rate": 12,
        "error": "Database connection timeout",
        "recent_change": "checkout-release-41",
        "description": "Checkout latency increased and database connections were exhausted.",
        "root_cause": "Connection pool exhaustion",
        "resolution": "Increase pool and restart affected workers",
        "result": "Checkout latency returned to normal",
    },
    {
        "incident_id": "INC-003",
        "service": "payment-api",
        "severity": "critical",
        "error_rate": 15,
        "error": "502 Bad Gateway",
        "recent_change": "payment-config-v1",
        "description": "Payment gateway errors followed a configuration modification.",
        "root_cause": "Incorrect upstream endpoint configuration",
        "resolution": "Rollback configuration",
        "result": "Error rate reduced from 15% to 2%",
    },
]

def seed_incidents():
    return len(INCIDENTS)

def list_incidents():
    return deepcopy(INCIDENTS)

def get_incident(incident_id):
    return next((deepcopy(x) for x in INCIDENTS if x["incident_id"] == incident_id), None)

def find_similar_incidents(incident):
    matches = []
    for old in INCIDENTS:
        if old["incident_id"] == incident.get("incident_id"):
            continue
        score = 0
        if old["service"] == incident.get("service"):
            score += 2
        if old["error"].lower() == incident.get("error", "").lower():
            score += 3
        if old["recent_change"] and incident.get("recent_change"):
            if "config" in old["recent_change"].lower() and "config" in incident["recent_change"].lower():
                score += 1
        if score >= 3:
            matches.append({**old, "similarity_score": score})
    return sorted(matches, key=lambda x: x["similarity_score"], reverse=True)
