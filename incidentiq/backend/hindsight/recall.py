from .memory import get_client, get_bank_id

def recall_incidents(query: str) -> list:
    response = get_client().recall(
        bank_id=get_bank_id(),
        query=query,
    )
    results = getattr(response, "results", None)
    if results is None and isinstance(response, dict):
        results = response.get("results", [])
    results = results or []

    output = []
    for item in results:
        if isinstance(item, dict):
            output.append(item)
        else:
            output.append({
                "id": getattr(item, "id", None),
                "text": getattr(item, "text", str(item)),
                "type": getattr(item, "type", None),
                "context": getattr(item, "context", None),
            })
    return output
