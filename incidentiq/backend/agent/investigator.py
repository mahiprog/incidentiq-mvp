def build_investigation(incident: dict, memories: list, local_matches: list) -> dict:
    evidence = []
    hypotheses = []

    if incident.get("recent_change"):
        evidence.append(f"Recent change detected: {incident['recent_change']}")
        hypotheses.append("The recent change may be related to the incident.")

    if incident.get("error_rate", 0) >= 10:
        evidence.append(f"High error rate: {incident['error_rate']}%")

    error = incident.get("error", "").lower()
    if "502" in error or "gateway" in error:
        hypotheses.append("Gateway/upstream service failure is a plausible cause.")
    if "timeout" in error:
        hypotheses.append("Upstream latency or connection saturation is a plausible cause.")
    if "database" in error or "connection" in error:
        hypotheses.append("Database connectivity/pool exhaustion is a plausible cause.")

    memory_insights = []
    for m in memories:
        text = m.get("text") or m.get("content") or str(m)
        if text:
            memory_insights.append(text)
            hypotheses.append(f"Historical experience: {text[:200]}")

    recommendation = (
        "Inspect the most recent change and compare its configuration/log signature "
        "with the recalled historical incidents before taking remediation."
        if not memory_insights else
        f"Based on {len(memory_insights)} recalled experience(s), prioritize the actions "
        "that resolved similar past incidents before trying new approaches."
    )

    return {
        "evidence": evidence,
        "hypotheses": hypotheses,
        "recommendation": recommendation,
        "memory_count": len(memories),
        "memory_insights": memory_insights,
        "local_match_count": len(local_matches),
    }
