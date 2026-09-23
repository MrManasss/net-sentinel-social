import { useEffect, useState } from "react";
import {
  createAuditChain,
  verifyAuditChain,
} from "../security/auditLog";

const records = [
  {
    postId: "post-001",
    content: "First social media post",
  },
  {
    postId: "post-002",
    content: "Second social media post",
  },
  {
    postId: "post-003",
    content: "Third social media post",
  },
];

function Dashboard() {
  const [chain, setChain] = useState([]);
  const [status, setStatus] = useState("CHECKING...");
  const [failedIndex, setFailedIndex] = useState(null);
  const [reason, setReason] = useState("");

  async function buildChain() {
    const newChain = await createAuditChain(records);

    setChain(newChain);

    const result = await verifyAuditChain(newChain);

    updateSecurityStatus(result);
  }

  async function verifyChain() {
    const result = await verifyAuditChain(chain);

    updateSecurityStatus(result);
  }

  function updateSecurityStatus(result) {
    if (result.valid) {
      setStatus("CHAIN VALID");
      setFailedIndex(null);
      setReason("All audit records passed integrity verification.");
    } else {
      setStatus("TAMPERING DETECTED");
      setFailedIndex(result.failedIndex);
      setReason(result.reason);
    }
  }

  function simulateTamper() {
    if (chain.length === 0) return;

    const tamperedChain = [...chain];

    tamperedChain[1] = {
      ...tamperedChain[1],
      data: {
        ...tamperedChain[1].data,
        content: "TAMPERED POST",
      },
    };

    setChain(tamperedChain);

    setStatus("TAMPERING SIMULATED");
    setFailedIndex(1);
    setReason("Audit record was modified after ingestion.");
  }

  async function restoreChain() {
    await buildChain();
  }

  useEffect(() => {
    buildChain();
  }, []);

  const chainIsValid = status === "CHAIN VALID";

  return (
    <div className="dashboard">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">⚡</div>

          <div>
            <h2>NET-SENTINEL</h2>
            <span>Social Intelligence</span>
          </div>
        </div>

        <div className="menu-title">
          MENU
        </div>

        <nav>

          <button className="nav-item active">
            ▣ Dashboard
          </button>

          <button className="nav-item">
            👥 Audience
          </button>

          <button className="nav-item">
            ◧ Content
          </button>

          <button className="nav-item">
            ◉ Network & Trends
          </button>

          <button className="nav-item">
            🔒 Integrity & Chain
          </button>

          <button className="nav-item">
            ▥ Reports
          </button>

        </nav>

        <div className="sidebar-footer">

          <div className="system-status">
            ● System Online
          </div>

          <small>
            NET-SENTINEL v1.0
          </small>

        </div>

      </aside>

      {/* MAIN */}

      <div className="main-area">

        <header className="topbar">

          <div>
            <h1>NET-SENTINEL</h1>

            <p>
              Social Network Intelligence & Security
            </p>
          </div>

          <div className="security-status">
            ● SYSTEM ONLINE
          </div>

        </header>

        <main className="dashboard-content">

          {/* KPI CARDS */}

          <section className="kpi-grid">

            <div className="card">
              <span>Total Posts</span>
              <strong>1,248</strong>
              <small>
                Across monitored channels
              </small>
            </div>

            <div className="card">
              <span>Security Alerts</span>
              <strong>42</strong>
              <small>
                Requires investigation
              </small>
            </div>

            <div className="card">
              <span>Total Reach</span>
              <strong>124K</strong>
              <small>
                Estimated audience
              </small>
            </div>

            <div className="card">
              <span>Engagement</span>
              <strong>6.82%</strong>
              <small>
                Current engagement rate
              </small>
            </div>

          </section>

          {/* ANALYSIS */}

          <section className="content-grid">

            <div className="panel">

              <h2>
                Network & Trend Analysis
              </h2>

              <p>
                Interaction and coordinated activity
              </p>

              <div className="placeholder">
                Network visualization
              </div>

            </div>

            <div className="panel">

              <h2>
                Sentiment Analysis
              </h2>

              <p>
                Audience sentiment distribution
              </p>

              <div className="placeholder">
                Sentiment chart
              </div>

            </div>

          </section>

          {/* SECURITY */}

          <section className="panel">

            <div className="panel-header">

              <div>
                <h2>
                  Security & Provenance
                </h2>

                <p>
                  SHA-256 audit-chain integrity
                </p>
              </div>

              <span
                className={
                  chainIsValid
                    ? "chain-valid"
                    : "chain-invalid"
                }
              >
                {chainIsValid
                  ? "✓ CHAIN VALID"
                  : "⚠ TAMPERING DETECTED"}
              </span>

            </div>

            {/* SECURITY SUMMARY */}

            <div className="security-summary">

              <div>
                <span>
                  Audit Records
                </span>

                <strong>
                  {chain.length}
                </strong>
              </div>

              <div>
                <span>
                  Integrity
                </span>

                <strong>
                  {chainIsValid
                    ? "Verified"
                    : "Failed"}
                </strong>
              </div>

              <div>
                <span>
                  Hash Algorithm
                </span>

                <strong>
                  SHA-256
                </strong>
              </div>

            </div>

            {/* SECURITY CONTROLS */}

            <div className="security-controls">

              <button
                className="security-button verify"
                onClick={verifyChain}
              >
                ✓ Verify Chain
              </button>

              <button
                className="security-button tamper"
                onClick={simulateTamper}
              >
                ⚠ Simulate Tamper
              </button>

              <button
                className="security-button restore"
                onClick={restoreChain}
              >
                ↻ Restore Chain
              </button>

            </div>

            {/* SECURITY MESSAGE */}

            {!chainIsValid && (
              <div className="security-alert">

                <strong>
                  Security Alert
                </strong>

                <p>
                  Affected Entry: #
                  {failedIndex}
                </p>

                <p>
                  Reason: {reason}
                </p>

              </div>
            )}

          </section>

        </main>

      </div>

    </div>
  );
}

export default Dashboard;