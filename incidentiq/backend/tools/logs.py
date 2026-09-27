def get_recent_logs(service: str):
    return [
        f"{service}: request started",
        f"{service}: upstream returned 502",
        f"{service}: error rate increased",
    ]
