import random

SERVICE_PROFILES = {
    "payment-api": {
        "base_error_rate": 18.0,
        "base_latency_ms": 840,
        "base_availability": 99.2,
        "recent_change": "payment-config-v4",
    },
    "checkout-api": {
        "base_error_rate": 12.0,
        "base_latency_ms": 620,
        "base_availability": 99.6,
        "recent_change": "checkout-release-41",
    },
}

DEFAULT_PROFILE = {
    "base_error_rate": 1.2,
    "base_latency_ms": 180,
    "base_availability": 99.95,
    "recent_change": "",
}

def get_metrics(service: str) -> dict:
    profile = SERVICE_PROFILES.get(service, DEFAULT_PROFILE)
    return {
        "service": service,
        "error_rate": round(profile["base_error_rate"] + random.uniform(-0.5, 0.5), 2),
        "latency_ms": int(profile["base_latency_ms"] + random.randint(-20, 20)),
        "availability": round(profile["base_availability"] + random.uniform(-0.05, 0.05), 3),
        "recent_change": profile["recent_change"],
    }
