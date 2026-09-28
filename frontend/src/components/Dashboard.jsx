import { useEffect, useState } from "react";
import {
  createAuditChain,
  verifyAuditChain,
} from "../security/auditLog";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

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

const networkData = [
  { day: "Mon", interactions: 420 },
  { day: "Tue", interactions: 580 },
  { day: "Wed", interactions: 510 },
  { day: "Thu", interactions: 760 },
  { day: "Fri", interactions: 690 },
  { day: "Sat", interactions: 920 },
  { day: "Sun", interactions: 840 },
];

const sentimentData = [
  { name: "Positive", value: 52 },
  { name: "Neutral", value: 31 },
  { name: "Negative", value: 17 },
];

const sentimentColors = [
  "#22c55e",
  "#64748b",
  "#ef4444",
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
              <span>Posts Analyzed</span>
              <strong>220</strong>
              <small>Across monitored channels</small>
            </div>

            <div className="card">
              <span>Campaign Accounts</span>
              <strong>18</strong>
              <small>Accounts linked to CAM-0017</small>
            </div>

            <div className="card">
              <span>Flagged Posts</span>
              <strong>42</strong>
              <small>Posts linked to the active campaign</small>
            </div>

            <div className="card">
              <span>Campaign Confidence</span>
              <strong>75%</strong>
              <small>Confidence score for CAM-0017</small>
            </div>

          </section>

          {/* ACTIVE INVESTIGATION */}

          <section className="investigation-panel">
            <div className="investigation-header">
              <div>
                <span className="eyebrow">ACTIVE INVESTIGATION</span>
                <h2>Coordinated Activity Detected</h2>
                <p>
                  Synchronized posting activity identified across multiple newly
                  activated accounts.
                </p>
              </div>

              <div className="investigation-status">
                <strong>HIGH</strong>
                <span>CAM-0017</span>
              </div>
            </div>

            <div className="investigation-details">
              <div>
                <span>Campaign</span>
                <strong>CAM-0017</strong>
              </div>

              <div>
                <span>Hashtag</span>
                <strong>#CyberSurakshaBill</strong>
              </div>

              <div>
                <span>Accounts</span>
                <strong>18</strong>
              </div>

              <div>
                <span>Posts</span>
                <strong>42</strong>
              </div>

              <div>
                <span>Confidence</span>
                <strong>75%</strong>
              </div>

              <div>
                <span>Decision State</span>
                <strong>ALERT &amp; NOTIFY</strong>
              </div>
            </div>
          </section>

          {/* ANALYSIS */}

          <section className="content-grid">

            <div className="panel">

              <h2>
                Activity Signal
              </h2>

              <p>
                Interaction volume across the monitored network
              </p>

              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={networkData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#263241" />
                    <XAxis
                      dataKey="day"
                      stroke="#7f8ea3"
                      tickLine={false}
                      axisLine={false}
                    />
                    <YAxis
                      stroke="#7f8ea3"
                      tickLine={false}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#10161f",
                        border: "1px solid #263241",
                        borderRadius: "8px",
                      }}
                    />
                    <Line
                      type="linear"
                      dataKey="interactions"
                      stroke="#55d6ff"
                      strokeWidth={2}
                      dot={false}
                      activeDot={{ r: 5 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

            </div>

            <div className="panel">

              <h2>
                Sentiment Analysis
              </h2>

              <p>
                Classified response distribution
              </p>

              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={sentimentData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="48%"
                      innerRadius={62}
                      outerRadius={88}
                      paddingAngle={2}
                    >
                      {sentimentData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={sentimentColors[index]}
                        />
                      ))}
                    </Pie>

                    <Tooltip />

                    <Legend
                      verticalAlign="bottom"
                      height={36}
                    />
                  </PieChart>
                </ResponsiveContainer>
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