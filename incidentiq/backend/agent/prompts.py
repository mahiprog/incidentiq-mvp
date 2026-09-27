def recommendation_prompt(incident: dict, investigation: dict) -> str:
    memories_section = ""
    if investigation.get("memory_insights"):
        formatted = "\n".join(f"- {m}" for m in investigation["memory_insights"])
        memories_section = f"\n\nRecalled historical experiences from Hindsight:\n{formatted}"
    else:
        memories_section = "\n\nNo historical memories recalled — this may be a novel incident."

    return f"""
You are IncidentIQ, an incident-response assistant that learns from past incidents.

Current incident:
{incident}

Investigation findings:
{investigation}{memories_section}

Using the recalled experiences as evidence (but not as guaranteed fixes),
recommend the safest next diagnostic or remediation step and explain why.
""".strip()
