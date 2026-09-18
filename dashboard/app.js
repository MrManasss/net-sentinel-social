/**
 * SocialPulse / Net-Sentinel Social — Modern SaaS Application Engine
 * Pixel-Accurate implementation based on modern Product Analytics UI
 */

let DEMO_DATA = null;
let currentNetwork = null;
let growthChart = null;
let donutChart = null;
let demoBarsChart = null;

let liveChain = [];
let originalChain = [];
let isTampered = false;

// ----------------------------------------------------------------------
// Pure JavaScript SHA-256 for Instant Offline & file:/// Execution
// ----------------------------------------------------------------------
function sha256Sync(ascii) {
  function rightRotate(value, amount) {
    return (value >>> amount) | (value << (32 - amount));
  }
  const mathPow = Math.pow;
  const maxWord = mathPow(2, 32);
  let lengthProperty = 'length';
  let i, j;
  let result = '';

  const words = [];
  const asciiBitLength = ascii[lengthProperty] * 8;

  let hash = sha256Sync.h = sha256Sync.h || [];
  let k = sha256Sync.k = sha256Sync.k || [];
  let primeCounter = k[lengthProperty];

  const isComposite = {};
  for (let candidate = 2; primeCounter < 64; candidate++) {
    if (!isComposite[candidate]) {
      for (i = 0; i < 300; i += candidate) {
        isComposite[i] = candidate;
      }
      hash[primeCounter] = (mathPow(candidate, 0.5) * maxWord) | 0;
      k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
    }
  }

  ascii += '\x80';
  while ((ascii[lengthProperty] % 64) - 56) ascii += '\x00';
  for (i = 0; i < ascii[lengthProperty]; i++) {
    j = ascii.charCodeAt(i);
    if (j >> 8) return;
    words[i >> 2] |= j << (((3 - i) % 4) * 8);
  }
  words[words[lengthProperty]] = (asciiBitLength / maxWord) | 0;
  words[words[lengthProperty]] = asciiBitLength;

  for (j = 0; j < words[lengthProperty];) {
    const w = words.slice(j, (j += 16));
    const oldHash = hash;
    hash = hash.slice(0, 8);

    for (i = 0; i < 64; i++) {
      const w15 = w[i - 15], w2 = w[i - 2];
      const s0 = rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3);
      const s1 = rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10);
      const ch = (hash[4] & hash[5]) ^ (~hash[4] & hash[6]);
      const maj = (hash[0] & hash[1]) ^ (hash[0] & hash[2]) ^ (hash[1] & hash[2]);
      const temp1 = hash[7] + (rightRotate(hash[4], 6) ^ rightRotate(hash[4], 11) ^ rightRotate(hash[4], 25)) + ch + k[i] + (w[i] = i < 16 ? w[i] : (w[i - 16] + s0 + w[i - 7] + s1) | 0);
      const temp2 = (rightRotate(hash[0], 2) ^ rightRotate(hash[0], 13) ^ rightRotate(hash[0], 22)) + maj;

      hash = [(temp1 + temp2) | 0].concat(hash);
      hash[4] = (hash[4] + temp1) | 0;
    }

    for (i = 0; i < 8; i++) {
      hash[i] = (hash[i] + oldHash[i]) | 0;
    }
  }

  for (i = 0; i < 8; i++) {
    for (let b = 3; b >= 0; b--) {
      const byte = (hash[i] >> (b * 8)) & 255;
      result += (byte < 16 ? '0' : '') + byte.toString(16);
    }
  }
  return result;
}

// ----------------------------------------------------------------------
// Chain Verification
// ----------------------------------------------------------------------
function verifyChainIntegrity(chain) {
  if (!chain || chain.length === 0) return { isValid: false, failedIndex: 0, message: "Chain is empty." };
  let expectedPrev = "0".repeat(64);

  for (let i = 0; i < chain.length; i++) {
    const block = chain[i];
    if (block.prev_hash !== expectedPrev) {
      return {
        isValid: false,
        failedIndex: i,
        message: `Broken cryptographic link at Block #${i}!`
      };
    }
    const blockPayload = `${block.index}:${block.timestamp}:${block.data_hash}:${block.prev_hash}`;
    const calculatedHash = sha256Sync(blockPayload);
    if (block.entry_hash !== calculatedHash) {
      return {
        isValid: false,
        failedIndex: i,
        message: `Tamper detected at Block #${i}! Entry hash altered.`
      };
    }
    expectedPrev = block.entry_hash;
  }
  return { isValid: true, failedIndex: null, message: `All ${chain.length} blocks valid.` };
}

// ----------------------------------------------------------------------
// Initialization
// ----------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  if (window.NET_SENTINEL_DEMO_DATA) {
    DEMO_DATA = window.NET_SENTINEL_DEMO_DATA;
    initSaaSApp();
  } else {
    fetch("demo_data.json")
      .then(res => res.json())
      .then(data => {
        DEMO_DATA = data;
        initSaaSApp();
      })
      .catch(err => {
        console.error("Data load failed:", err);
      });
  }
});

function initSaaSApp() {
  originalChain = JSON.parse(JSON.stringify(DEMO_DATA.hash_chain.chain));
  liveChain = JSON.parse(JSON.stringify(DEMO_DATA.hash_chain.chain));

  initEventListeners();
  initAudienceGrowthChart();
  initSentimentDonut();
  initDemographicsBars();
  initNetworkVisualization();
  renderAuditTable();
}

// ----------------------------------------------------------------------
// Charts Implementation (Exact Match to PDF Reference)
// ----------------------------------------------------------------------

// 1. Audience Growth (Dual Line Chart: Followers vs Reach)
function initAudienceGrowthChart() {
  const ctx = document.getElementById("chart-audience-growth");
  if (!ctx || !window.Chart) return;

  const labels = ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6", "Wk7", "Wk8"];
  const followersData = [840, 855, 870, 890, 915, 930, 950, 975];
  const reachData = [240, 260, 290, 310, 340, 380, 420, 480];

  growthChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Followers",
          data: followersData,
          borderColor: "#5e52ea",
          backgroundColor: "rgba(94, 82, 234, 0.04)",
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 0,
          pointHoverRadius: 4,
          fill: true
        },
        {
          label: "Reach",
          data: reachData,
          borderColor: "#38bdf8",
          backgroundColor: "transparent",
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.35,
          pointRadius: 0,
          pointHoverRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: "#8e8ba6", font: { size: 10.5, family: "sans-serif" } }
        },
        y: {
          min: 0,
          max: 1000,
          ticks: {
            stepSize: 200,
            color: "#8e8ba6",
            font: { size: 10, family: "sans-serif" }
          },
          grid: { color: "#edf0f7" }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#16142a",
          padding: 10,
          cornerRadius: 8
        }
      }
    }
  });
}

// 2. Sentiment Analysis Donut (Vibrant Thick Ring matching PDF)
function initSentimentDonut() {
  const ctx = document.getElementById("chart-sentiment-donut");
  if (!ctx || !window.Chart) return;

  donutChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Positive / Supportive", "Neutral", "Negative / Critical"],
      datasets: [{
        data: [68, 24, 8],
        backgroundColor: ["#5e52ea", "#38bdf8", "#ec4899"],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "74%",
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#16142a",
          padding: 8,
          cornerRadius: 6,
          callbacks: {
            label: (item) => ` ${item.label}: ${item.raw}%`
          }
        }
      }
    }
  });
}

// 3. Audience Demographics Vertical Bars (matching PDF Bottom-Right)
function initDemographicsBars() {
  const ctx = document.getElementById("chart-demographics-bars");
  if (!ctx || !window.Chart) return;

  const labels = ["18-24", "25-34", "35-44", "45-54", "55+"];
  const counts = [12, 42, 24, 8, 4];

  demoBarsChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        data: counts,
        backgroundColor: "#b4b1fc",
        hoverBackgroundColor: "#5e52ea",
        borderRadius: 4,
        barThickness: 22
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: "#8e8ba6", font: { size: 10 } }
        },
        y: {
          max: 50,
          ticks: { stepSize: 10, color: "#8e8ba6", font: { size: 9 } },
          grid: { color: "#f1f5f9" }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

// 4. Network Force-Directed Graph (vis-network)
function initNetworkVisualization() {
  const container = document.getElementById("vis-network-div");
  if (!container || !window.vis || !DEMO_DATA) return;

  const netData = DEMO_DATA.network.visualization;
  
  // Custom styled nodes for light theme
  const styledNodes = netData.nodes.map(n => ({
    id: n.id,
    label: n.label,
    value: n.value,
    color: n.is_bot ? "#ef4444" : (n.value > 15 ? "#5e52ea" : "#94a3b8"),
    shape: "dot",
    font: { size: 9, color: "#475569" }
  }));

  const styledEdges = netData.edges_full.map(e => ({
    from: e.from,
    to: e.to,
    color: { color: "#e2e8f0", highlight: "#5e52ea" },
    width: 1
  }));

  const options = {
    physics: {
      stabilization: { iterations: 80 },
      barnesHut: { gravitationalConstant: -1400, springLength: 70 }
    },
    interaction: { hover: true }
  };

  currentNetwork = new vis.Network(container, {
    nodes: new vis.DataSet(styledNodes),
    edges: new vis.DataSet(styledEdges)
  }, options);
}

// ----------------------------------------------------------------------
// Tamper Lab Execution (F-10)
// ----------------------------------------------------------------------
function renderAuditTable() {
  const tbody = document.getElementById("audit-log-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  const sample = liveChain.slice(0, 8);
  sample.forEach(b => {
    const tr = document.createElement("tr");
    const isRowTampered = isTampered && b.index === 5;
    if (isRowTampered) tr.className = "tampered-table-row";

    tr.innerHTML = `
      <td>#${b.index}</td>
      <td>${b.timestamp.slice(11, 19)}</td>
      <td>${b.post_id}</td>
      <td>${b.author_handle}</td>
      <td>${b.data_hash.slice(0, 14)}...</td>
      <td>${b.entry_hash.slice(0, 14)}...</td>
      <td>${isRowTampered ? '<span class="badge-chain-tamper">⚠ TAMPERED</span>' : '<span class="badge-chain-clean">✓ VALID</span>'}</td>
    `;
    tbody.appendChild(tr);
  });
}

function simulateTamper() {
  isTampered = true;
  liveChain[5].data_hash = sha256Sync("MODIFIED_UNAUTHORIZED_CONTENT");

  const alertBox = document.getElementById("tamper-alert-box");
  if (alertBox) alertBox.classList.remove("hidden");

  renderAuditTable();
}

function restoreChain() {
  isTampered = false;
  liveChain = JSON.parse(JSON.stringify(originalChain));

  const alertBox = document.getElementById("tamper-alert-box");
  if (alertBox) alertBox.classList.add("hidden");

  renderAuditTable();
}

// ----------------------------------------------------------------------
// Event Listeners
// ----------------------------------------------------------------------
function initEventListeners() {
  // Tamper buttons
  document.getElementById("btn-simulate-tamper")?.addEventListener("click", simulateTamper);
  document.getElementById("btn-restore-chain")?.addEventListener("click", restoreChain);

  // Modals
  const invModal = document.getElementById("investigation-modal");
  const reportModal = document.getElementById("report-modal");

  document.getElementById("btn-open-investigation")?.addEventListener("click", () => {
    populateEvidenceStream();
    invModal.classList.remove("hidden");
  });
  document.getElementById("btn-close-inv")?.addEventListener("click", () => invModal.classList.add("hidden"));
  document.getElementById("btn-close-inv-action")?.addEventListener("click", () => invModal.classList.add("hidden"));

  document.getElementById("btn-export-report")?.addEventListener("click", () => reportModal.classList.remove("hidden"));
  document.getElementById("nav-reports")?.addEventListener("click", () => reportModal.classList.remove("hidden"));
  document.getElementById("btn-close-report")?.addEventListener("click", () => reportModal.classList.add("hidden"));
  document.getElementById("btn-close-report-action")?.addEventListener("click", () => reportModal.classList.add("hidden"));

  // View all posts triggers investigation drawer
  document.getElementById("link-view-all-posts")?.addEventListener("click", () => {
    populateEvidenceStream();
    invModal.classList.remove("hidden");
  });

  // Network snapshot toggles
  document.getElementById("btn-net-before")?.addEventListener("click", (e) => {
    e.target.classList.add("active");
    document.getElementById("btn-net-after").classList.remove("active");
    switchNetwork("before");
  });

  document.getElementById("btn-net-after")?.addEventListener("click", (e) => {
    e.target.classList.add("active");
    document.getElementById("btn-net-before").classList.remove("active");
    switchNetwork("after");
  });

  // Time range pills
  document.querySelectorAll(".range-pill").forEach(pill => {
    pill.addEventListener("click", (e) => {
      document.querySelectorAll(".range-pill").forEach(p => p.classList.remove("active"));
      e.target.classList.add("active");
    });
  });

  // Platform pills
  document.querySelectorAll(".platform-pill").forEach(pill => {
    pill.addEventListener("click", (e) => {
      document.querySelectorAll(".platform-pill").forEach(p => p.classList.remove("pill-active-dark"));
      e.target.classList.add("pill-active-dark");
    });
  });
}

function switchNetwork(snapshot) {
  if (!currentNetwork || !DEMO_DATA) return;
  const netData = DEMO_DATA.network.visualization;

  if (snapshot === "before") {
    const organicNodes = netData.nodes.filter(n => !n.is_bot).map(n => ({
      id: n.id, label: n.label, value: n.value, color: n.value > 15 ? "#5e52ea" : "#94a3b8", shape: "dot"
    }));
    currentNetwork.setData({
      nodes: new vis.DataSet(organicNodes),
      edges: new vis.DataSet(netData.edges_before)
    });
  } else {
    const allNodes = netData.nodes.map(n => ({
      id: n.id, label: n.label, value: n.value, color: n.is_bot ? "#ef4444" : (n.value > 15 ? "#5e52ea" : "#94a3b8"), shape: "dot"
    }));
    currentNetwork.setData({
      nodes: new vis.DataSet(allNodes),
      edges: new vis.DataSet(netData.edges_full)
    });
  }
}

function populateEvidenceStream() {
  const stream = document.getElementById("evidence-posts-stream");
  if (!stream || !DEMO_DATA) return;
  stream.innerHTML = "";

  const sample = DEMO_DATA.campaign.sample_evidence_posts || [];
  sample.forEach(p => {
    const card = document.createElement("div");
    card.style = "background:#f8fafc; border:1px solid #e2e8f0; border-left:3px solid #ef4444; border-radius:8px; padding:10px 14px;";
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.75rem; color:#64748b;">
        <strong style="color:#5e52ea;">${p.author_handle}</strong>
        <span>${p.platform.toUpperCase()} • ${p.timestamp.slice(11, 19)}</span>
      </div>
      <div style="font-size:0.82rem; color:#1e293b; margin-bottom:6px;">${p.text}</div>
      <div style="font-size:0.72rem; color:#94a3b8;">Engagement: ${p.engagement.likes} likes • ${p.engagement.shares} retweets</div>
    `;
    stream.appendChild(card);
  });
}
