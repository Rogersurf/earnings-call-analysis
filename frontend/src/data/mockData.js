/* ====================================================== */
/* GRAPH NODES */
/* ====================================================== */

export const initialNodes = [

  /* SIGNALS */

  {
    id: "signal_ai",
    type: "signal",
    position: { x: 80, y: 300 },
    data: {
      label: "AI Demand ↑",
      signal: "High Propagation",
    },
  },

  {
    id: "signal_energy",
    type: "signal",
    position: { x: 150, y: 600 },
    data: {
      label: "Power Stress",
      signal: "Grid Pressure",
    },
  },

  /* SEMICONDUCTORS */

  {
    id: "nvda",
    type: "company",
    position: { x: 350, y: 250 },
    data: {
      label: "NVIDIA",
      sector: "Semiconductors",
      signal: "Demand Surge",
    },
  },

  {
    id: "amd",
    type: "company",
    position: { x: 450, y: 480 },
    data: {
      label: "AMD",
      sector: "Semiconductors",
      signal: "Inventory Build",
    },
  },

  {
    id: "tsmc",
    type: "company",
    position: { x: 620, y: 320 },
    data: {
      label: "TSMC",
      sector: "Semiconductors",
      signal: "Capacity Stress",
    },
  },

  {
    id: "intel",
    type: "company",
    position: { x: 520, y: 120 },
    data: {
      label: "Intel",
      sector: "Semiconductors",
      signal: "Foundry Expansion",
    },
  },

  /* CLOUD */

  {
    id: "aws",
    type: "company",
    position: { x: 950, y: 180 },
    data: {
      label: "AWS",
      sector: "Cloud",
      signal: "AI Infrastructure",
    },
  },

  {
    id: "azure",
    type: "company",
    position: { x: 1020, y: 420 },
    data: {
      label: "Azure",
      sector: "Cloud",
      signal: "Compute Scaling",
    },
  },

  {
    id: "google_cloud",
    type: "company",
    position: { x: 850, y: 580 },
    data: {
      label: "Google Cloud",
      sector: "Cloud",
      signal: "Inference Growth",
    },
  },

  /* ENERGY */

  {
    id: "grid",
    type: "sector",
    position: { x: 1300, y: 350 },
    data: {
      label: "Power Grid",
      sector: "Energy",
      signal: "Consumption Spike",
    },
  },

  {
    id: "energy_sector",
    type: "sector",
    position: { x: 1450, y: 520 },
    data: {
      label: "Energy Sector",
      sector: "Energy",
      signal: "Infrastructure Stress",
    },
  },

  /* LOGISTICS */

  {
    id: "logistics",
    type: "sector",
    position: { x: 1200, y: 700 },
    data: {
      label: "Logistics Network",
      sector: "Supply Chain",
      signal: "Capacity Bottleneck",
    },
  },

  /* RETAIL */

  {
    id: "retail",
    type: "sector",
    position: { x: 850, y: 850 },
    data: {
      label: "Retail Sector",
      sector: "Retail",
      signal: "Demand Weakness",
    },
  },

];

/* ====================================================== */
/* EDGES */
/* ====================================================== */

export const initialEdges = [

  {
    id: "e1",
    source: "signal_ai",
    target: "nvda",
    animated: true,
    style: {
      stroke: "#00e5ff",
    },
    label: "AI demand",
  },

  {
    id: "e2",
    source: "nvda",
    target: "tsmc",
    animated: true,
    style: {
      stroke: "#00e5ff",
    },
    label: "chip orders",
  },

  {
    id: "e3",
    source: "tsmc",
    target: "intel",
    animated: true,
    style: {
      stroke: "#a855f7",
    },
    label: "foundry competition",
  },

  {
    id: "e4",
    source: "nvda",
    target: "aws",
    animated: true,
    style: {
      stroke: "#22c55e",
    },
    label: "GPU demand",
  },

  {
    id: "e5",
    source: "aws",
    target: "grid",
    animated: true,
    style: {
      stroke: "#ff6b6b",
    },
    label: "power consumption",
  },

  {
    id: "e6",
    source: "azure",
    target: "grid",
    animated: true,
    style: {
      stroke: "#ff6b6b",
    },
    label: "energy pressure",
  },

  {
    id: "e7",
    source: "google_cloud",
    target: "grid",
    animated: true,
    style: {
      stroke: "#ff6b6b",
    },
    label: "AI infrastructure",
  },

  {
    id: "e8",
    source: "signal_energy",
    target: "grid",
    animated: true,
    style: {
      stroke: "#facc15",
    },
    label: "grid instability",
  },

  {
    id: "e9",
    source: "grid",
    target: "energy_sector",
    animated: true,
    style: {
      stroke: "#f97316",
    },
    label: "propagation",
  },

  {
    id: "e10",
    source: "energy_sector",
    target: "logistics",
    animated: true,
    style: {
      stroke: "#22c55e",
    },
    label: "fuel pressure",
  },

  {
    id: "e11",
    source: "logistics",
    target: "retail",
    animated: true,
    style: {
      stroke: "#a855f7",
    },
    label: "distribution slowdown",
  },

  {
    id: "e12",
    source: "amd",
    target: "azure",
    animated: true,
    style: {
      stroke: "#00e5ff",
    },
    label: "accelerator supply",
  },

];

/* ====================================================== */
/* AI AGENTS */
/* ====================================================== */

export const agentStreamMock = [

  {
    agent: "SupplyChainAgent",
    message:
      "TSMC backlog increasing after NVIDIA demand acceleration.",
    confidence: 0.92,
    type: "warning",
  },

  {
    agent: "EnergyGridAgent",
    message:
      "Cloud infrastructure expansion impacting regional power stability.",
    confidence: 0.88,
    type: "alert",
  },

  {
    agent: "SemanticPropagationAgent",
    message:
      "Detected cross-sector propagation from semiconductors into logistics.",
    confidence: 0.95,
    type: "info",
  },

  {
    agent: "MarketSentimentAgent",
    message:
      "Management tone remains bullish across AI infrastructure calls.",
    confidence: 0.81,
    type: "info",
  },

  {
    agent: "AnomalyDetectionAgent",
    message:
      "Unexpected divergence detected in retail demand guidance.",
    confidence: 0.74,
    type: "warning",
  },

  {
    agent: "ConsensusEngine",
    message:
      "High probability of continued infrastructure stress through next quarter.",
    confidence: 0.93,
    type: "alert",
  },

];

/* ====================================================== */
/* TIMELINE */
/* ====================================================== */

export const propagationTimeline = [

  {
    quarter: "Q1 2024",
    event:
      "NVIDIA reports explosive AI accelerator demand.",
    target: "Semiconductors",
  },

  {
    quarter: "Q2 2024",
    event:
      "TSMC manufacturing capacity reaches critical utilization.",
    target: "Semiconductors",
  },

  {
    quarter: "Q3 2024",
    event:
      "Cloud hyperscalers accelerate infrastructure investments.",
    target: "Cloud",
  },

  {
    quarter: "Q4 2024",
    event:
      "Power grid stress increases due to AI compute expansion.",
    target: "Energy",
  },

  {
    quarter: "Q1 2025",
    event:
      "Logistics and distribution networks experience bottlenecks.",
    target: "Hardware",
  },

];

/* ====================================================== */
/* MARKET FEED */
/* ====================================================== */

export const marketFeed = [

  {
    title:
      "NVIDIA Q2 earnings surpass expectations",
    time: "2m ago",
    impact: "High",
  },

  {
    title:
      "TSMC warns about AI capacity constraints",
    time: "8m ago",
    impact: "Critical",
  },

  {
    title:
      "Microsoft expands Azure AI infrastructure",
    time: "15m ago",
    impact: "Medium",
  },

  {
    title:
      "Energy demand rises across AI datacenters",
    time: "27m ago",
    impact: "High",
  },

  {
    title:
      "Amazon increases AI capex forecast",
    time: "41m ago",
    impact: "Medium",
  },

];

/* ====================================================== */
/* TRANSCRIPT FEED */
/* ====================================================== */

export const transcriptFeed = [

  {
    company: "NVIDIA",
    quarter: "Q2 2025",
    status: "New",
  },

  {
    company: "TSMC",
    quarter: "Q1 2025",
    status: "Analyzed",
  },

  {
    company: "AMD",
    quarter: "Q1 2025",
    status: "Processing",
  },

  {
    company: "Microsoft",
    quarter: "Q2 2025",
    status: "New",
  },

  {
    company: "Amazon",
    quarter: "Q2 2025",
    status: "Analyzed",
  },

];

/* ====================================================== */
/* KPI STATS */
/* ====================================================== */

export const topBarStats = {

  live: true,

  transcripts: 9069,

  agentsActive: 6,

  alerts: 4,

  anomalies: 2,

};