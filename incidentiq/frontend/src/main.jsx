import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "http://localhost:8000";
const SERVICES = ["payment-api", "checkout-api"];

const STEPS = ["idle", "detected", "investigated", "approved", "resolved"];

function App() {
  const [service, setService] = useState("payment-api");
  const [step, setStep] = useState("idle");
  const [loading, setLoading] = useState(false);
  const [incident, setIncident] = useState(null);
  const [investigation, setInvestigation] = useState(null);
  const [memories, setMemories] = useState([]);
  const [localMatches, setLocalMatches] = useState([]);
  const [error, setError] = useState(null);

  async function runFullPipeline() {
    setLoading(true);
    setError(null);
    setStep("idle");
    setIncident(null);
    setInvestigation(null);
    setMemories([]);
    setLocalMatches([]);
    try {
      const res = await fetch(`${API}/monitor/${service}/investigate`);
      const data = await res.json();
      if (data.status === "healthy") {
        setError("✓ All systems healthy — no incident detected.");
        setStep("idle");
        return;
      }
      setIncident(data.incident);
      setInvestigation(data.investigation);
      setMemories(data.historical_memories || []);
      setLocalMatches(data.local_matches || []);
      setStep("investigated");
    } catch (e) {
      setError("Backend unavailable. Start FastAPI on port 8000.");
    } finally {
      setLoading(false);
    }
  }

  async function resolveAndRetain() {
    setLoading(true);
    try {
      const res = await fetch(`${API}/incidents/${incident.incident_id}/resolve`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          incident_id: incident.incident_id,
          action: investigation.recommendation,
          result: "Incident resolved following AI recommendation.",
          service: incident.service,
          error: incident.error,
        })
      });
      if (!res.ok) throw new Error(await res.text());
      setStep("resolved");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const stepIndex = STEPS.indexOf(step);

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

        {/* Pipeline Steps */}
        <section className="card">
          <h2>Pipeline</h2>
          <div className="pipeline">
            {["Detect", "Investigate + Recall", "Human Approval", "Resolve + Retain"].map((s, i) => (
              <div key={i} className={`pipeline-step ${stepIndex > i ? "done" : stepIndex === i + 1 ? "active" : ""}`}>
                <div className="step-dot">{stepIndex > i ? "✓" : i + 1}</div>
                <span>{s}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Detection */}
        <section className="card">
          <h2>Live Application Monitor</h2>
          <p>Select a service and run detection against live metrics and logs.</p>
          <div className="monitor-bar">
            <select value={service} onChange={e => setService(e.target.value)}>
              {SERVICES.map(s => <option key={s}>{s}</option>)}
            </select>
            <button onClick={runFullPipeline} disabled={loading} style={{marginTop:0}}>
              {loading ? "Running pipeline..." : "▶ Run Detection"}
            </button>
          </div>
          {error && <div className="alert-healthy" style={{marginTop:14}}>{error}</div>}
        </section>

        {/* Incident Detected */}
        {incident && (
          <section className="card">
            <div className="section-title">
              <h2>🚨 Incident Detected</h2>
              <span className={`pill ${incident.severity === "critical" ? "pill-critical" : "pill-high"}`}>
                {incident.severity.toUpperCase()}
              </span>
            </div>
            <div className="metric-grid">
              <div className="metric"><span>ID</span><strong>{incident.incident_id}</strong></div>
              <div className="metric"><span>Service</span><strong>{incident.service}</strong></div>
              <div className="metric"><span>Error Rate</span><strong>{incident.error_rate}%</strong></div>
              <div className="metric"><span>Error</span><strong>{incident.error}</strong></div>
            </div>
            {incident.recent_change && <p style={{marginTop:12}}>Recent change: <strong>{incident.recent_change}</strong></p>}
            <h3>Logs</h3>
            <ul>{incident.logs?.map((l,i) => <li key={i}>{l}</li>)}</ul>
          </section>
        )}

        {/* Investigation + Recall */}
        {investigation && (
          <section className="card">
            <div className="section-title">
              <h2>AI Investigation</h2>
              <span className="pill">{investigation.memory_count} historical memories</span>
            </div>
            <h3>Evidence</h3>
            <ul>{investigation.evidence.map((x,i) => <li key={i}>{x}</li>)}</ul>
            <h3>Hypotheses</h3>
            <ul>{investigation.hypotheses.map((x,i) => <li key={i}>{x}</li>)}</ul>

            {memories.length > 0 && (
              <>
                <h3>Recalled from Hindsight</h3>
                {memories.map((m,i) => (
                  <div className="memory hindsight" key={i}>
                    <strong>Past Experience #{i+1}</strong>
                    <p>{m.text || JSON.stringify(m)}</p>
                  </div>
                ))}
              </>
            )}

            {localMatches.length > 0 && (
              <>
                <h3>Local Similar Incidents</h3>
                {localMatches.map(x => (
                  <div className="memory" key={x.incident_id}>
                    <strong>{x.incident_id} — {x.service}</strong>
                    <p>{x.error}</p>
                    <small>Resolution: {x.resolution}</small>
                  </div>
                ))}
              </>
            )}

            <div className="recommendation">
              <strong>AI Recommendation</strong>
              <p>{investigation.recommendation}</p>
            </div>
          </section>
        )}

        {/* Human Approval */}
        {investigation && step !== "resolved" && (
          <section className="card">
            <h2>Human Approval</h2>
            <p>Review the AI recommendation above. Approve to execute resolution and store the outcome in Hindsight.</p>
            <div className="monitor-bar">
              <button onClick={() => setStep("approved")} disabled={step === "approved" || loading} style={{marginTop:0, background:"#3ecf8e", color:"#071024"}}>
                ✓ Approve & Execute
              </button>
              <button onClick={resolveAndRetain} disabled={step !== "approved" || loading} style={{marginTop:0}}>
                {loading ? "Storing..." : "Resolve & Remember"}
              </button>
            </div>
            {step === "approved" && <div className="alert-healthy" style={{marginTop:12}}>Approved. Click Resolve & Remember to store in Hindsight.</div>}
          </section>
        )}

        {/* Resolved */}
        {step === "resolved" && (
          <section className="card">
            <div className="success">
              ✓ Resolution stored in Hindsight. This experience will be recalled for future similar incidents.
            </div>
          </section>
        )}

      </main>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
