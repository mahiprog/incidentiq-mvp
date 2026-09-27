from .memory import get_client, get_bank_id

def retain_incident(payload: dict):
    content = f"""
Incident ID: {payload['incident_id']}
Service: {payload.get('service', 'unknown')}
Error: {payload.get('error', 'unknown')}
Action taken: {payload['action']}
Result: {payload['result']}
This is an organizational incident-response experience. Remember the problem,
decision, action, and observed outcome for future similar incidents.
""".strip()

    response = get_client().retain(
        bank_id=get_bank_id(),
        content=content,
        context="production incident resolution",
        document_id=payload["incident_id"],
        metadata={"type": "incident_resolution"},
        tags=["incident", payload.get("service", ""), payload["incident_id"]],
    )
    return str(response)
