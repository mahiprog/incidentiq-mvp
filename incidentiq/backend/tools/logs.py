SERVICE_LOGS = {
    "payment-api": [
        "payment-api: health check started",
        "payment-api: upstream returned 502 Bad Gateway",
        "payment-api: retry attempt 1 of 3",
        "payment-api: retry attempt 2 of 3",
        "payment-api: error rate crossed 15% threshold",
        "payment-api: alert triggered — configuration mismatch suspected",
    ],
    "checkout-api": [
        "checkout-api: health check started",
        "checkout-api: database connection pool exhausted",
        "checkout-api: query timeout after 30s",
        "checkout-api: worker restart attempted",
        "checkout-api: latency p99 exceeded 600ms",
    ],
}

DEFAULT_LOGS = [
    "{service}: health check started",
    "{service}: all systems nominal",
]

def get_recent_logs(service: str) -> list:
    logs = SERVICE_LOGS.get(service)
    if logs:
        return logs
    return [l.format(service=service) for l in DEFAULT_LOGS]
