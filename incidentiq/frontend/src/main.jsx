import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "http://localhost:8000";

const initial = {
  incident_id: "INC-004",
  service: "payment-api",
  severity: "critical",
  error_rate: 18,
  error: "502 Bad Gateway",
  recent_change: "payment-config-v4",
  description: "Payment failures increased shortly after a configuration deployment."
};

function App() {
  const [incident, setIncident] = useState(initial);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [resolved, setResolved] = useState(false);

  async function investigate() {
    setLoading(true);
    setResolved(false);
    try {
      const res = await fetch(`${API}/investigate`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(incident)
      });
      setResult(await res.json());
    } catch (e) {
      setResult({error: "Backend unavailable. Start FastAPI on port 8000."});
    } finally {
      setLoading(false);
    }
  }

  async function resolve() {
    try {
      const res = await fetch(`${API}/incidents/${incident.incident_id}/resolve`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          incident_id: incident.incident_id,
          action: "Rollback latest payment configuration",
          result: "Error rate reduced from 18% to 1%",
          service: incident.service,
          error: incident.error
        })
      });
      if (!res.ok) throw new Error(await res.text());
      setResolved(true);
    } catch (e) {
      alert(e.message);
    }
  }

  return (
    <div className="app">
      <header>
        <div>
          <div className="eyebrow">AUTONOMOUS INCIDENT RESPONSE</div>
          <h1>IncidentIQ</h1>
          <p>Your engineering team's memory for every incident.</p>
        </div>
        <div className="badge">HINDSIGHT MEMORY</div>
      </header>

      <main>
        <section className="card">
          <h2>Current Incident</h2>
          <div className="grid">
            <label>Incident ID<input value={incident.incident_id} onChange={e => setIncident({...incident, incident_id:e.target.value})}/></label>
            <label>Service<input value={incident.service} onChange={e => setIncident({...incident, service:e.target.value})}/></label>
            <label>Error Rate (%)<input type="number" value={incident.error_rate} onChange={e => setIncident({...incident, error_rate:Number(e.target.value)})}/></label>
            <label>Recent Change<input value={incident.recent_change} onChange={e => setIncident({...incident, recent_change:e.target.value})}/></label>
          </div>
          <label>Error<input value={incident.error} onChange={e => setIncident({...incident, error:e.target.value})}/></label>
          <label>Description<textarea value={incident.description} onChange={e => setIncident({...incident, description:e.target.value})}/></label>
          <button onClick={investigate} disabled={loading}>{loading ? "Investigating..." : "Investigate Incident"}</button>
        </section>

        {result && !result.error && (
          <>
            <section className="card">
              <div className="section-title">
                <h2>AI Investigation</h2>
                <span className="pill">{result.investigation.memory_count} historical memories</span>
              </div>
              <h3>Evidence</h3>
              <ul>{result.investigation.evidence.map((x,i)=><li key={i}>{x}</li>)}</ul>
              <h3>Hypotheses</h3>
              <ul>{result.investigation.hypotheses.map((x,i)=><li key={i}>{x}</li>)}</ul>
              {result.investigation.memory_insights && result.investigation.memory_insights.length > 0 && (
                <div>
                  <h3>Recalled from Hindsight</h3>
                  {result.investigation.memory_insights.map((m,i) => (
                    <div className="memory hindsight" key={i}>
                      <strong>Past Experience #{i+1}</strong>
                      <p>{m}</p>
                    </div>
                  ))}
                </div>
              )}
              <div className="recommendation">
                <strong>Recommendation</strong>
                <p>{result.investigation.recommendation}</p>
              </div>
            </section>

            <section className="card">
              <h2>Historical Experience</h2>
              {result.local_matches.length === 0 ? (
                <p>No local similar incident found.</p>
              ) : result.local_matches.map(x => (
                <div className="memory" key={x.incident_id}>
                  <strong>{x.incident_id} — {x.service}</strong>
                  <p>{x.error}</p>
                  <small>Resolution: {x.resolution}</small>
                  <small>Result: {x.result}</small>
                </div>
              ))}
              {result.historical_memories.map((x,i) => (
                <div className="memory hindsight" key={i}>
                  <strong>Hindsight memory</strong>
                  <p>{x.text || JSON.stringify(x)}</p>
                </div>
              ))}
            </section>

            <section className="card">
              <h2>Resolution</h2>
              <p>For the demo, simulate the recommended rollback and store the outcome in Hindsight.</p>
              <button onClick={resolve} disabled={resolved}>{resolved ? "✓ Resolution Stored" : "Resolve & Remember"}</button>
              {resolved && <div className="success">New organizational experience retained in Hindsight.</div>}
            </section>
          </>
        )}

        {result?.error && <section className="card error">{result.error}</section>}
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
