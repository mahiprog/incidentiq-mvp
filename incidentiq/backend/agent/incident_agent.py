from backend.hindsight.recall import recall_incidents
from backend.tools.incidents import find_similar_incidents
from backend.agent.investigator import build_investigation
from backend.agent.prompts import recommendation_prompt

def investigate_incident(incident: dict) -> dict:
    query = (
        f"service={incident['service']}; "
        f"error={incident['error']}; "
        f"recent_change={incident.get('recent_change','')}; "
        f"description={incident.get('description','')}"
    )

    memories = recall_incidents(query)
    local_matches = find_similar_incidents(incident)
    investigation = build_investigation(incident, memories, local_matches)

    return {
        "incident": incident,
        "investigation": investigation,
        "historical_memories": memories,
        "local_matches": local_matches,
        "recommendation_prompt": recommendation_prompt(incident, investigation),
    }
