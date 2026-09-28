-- IncidentIQ Incident Schema
-- Reference schema for persistent incident storage

CREATE TABLE IF NOT EXISTS incidents (
    id          SERIAL PRIMARY KEY,
    incident_id VARCHAR(64) UNIQUE NOT NULL,
    service     VARCHAR(128) NOT NULL,
    severity    VARCHAR(32) NOT NULL,
    error_rate  NUMERIC(5,2) NOT NULL,
    error       TEXT NOT NULL,
    recent_change VARCHAR(256),
    description TEXT,
    root_cause  TEXT,
    resolution  TEXT,
    result      TEXT,
    created_at  TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS memories (
    id          SERIAL PRIMARY KEY,
    incident_id VARCHAR(64) REFERENCES incidents(incident_id),
    action      TEXT NOT NULL,
    result      TEXT NOT NULL,
    hindsight_doc_id VARCHAR(256),
    retained_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_incidents_service ON incidents(service);
CREATE INDEX idx_incidents_severity ON incidents(severity);
CREATE INDEX idx_memories_incident ON memories(incident_id);
