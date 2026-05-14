# 🚀 Earnings Call Semantic Intelligence Platform

A scalable AI and data engineering platform focused on:

- 📥 Earnings call transcript collection
- 🧹 NLP-oriented cleaning and normalization
- 🧠 Semantic intelligence extraction
- 🌐 Knowledge graph generation
- 🤖 Multi-agent financial reasoning
- 📊 Interactive AI dashboards
- 🔎 RAG and semantic search systems

# 🌐 Live Dashboard Demo

The enterprise semantic intelligence dashboard is deployed on Vercel and can be accessed here:

```text
https://earnings-call-analysis-xi.vercel.app/
```

The dashboard currently includes:

- 🌐 Semantic propagation graph
- 🤖 Multi-agent reasoning stream
- 📈 Sector heatmaps
- ⏳ Temporal propagation timeline
- 🚨 Financial anomaly alerts
- 📡 Real-time intelligence panels
- 🔎 Future RAG integration structure

Frontend stack:

- ⚛️ React
- ⚡ Vite
- 🎨 TailwindCSS
- 🎞️ Framer Motion
- 🌐 React Flow

The interface was designed to resemble modern enterprise intelligence platforms such as:

- Bloomberg Terminal
- Palantir Foundry
- AI-powered financial monitoring systems

The platform transforms raw earnings call transcripts into a structured semantic intelligence ecosystem ready for:

- LLMs
- Embeddings
- RAG systems
- Semantic search
- Financial NLP
- Knowledge graphs
- Multi-agent AI systems
- Enterprise dashboards

---

# 📊 Dataset Overview

| Metric | Value |
|---|---|
| 📄 Total Transcripts | 9,069 |
| 🏢 Unique Tickers | 2,944 |
| 📅 Coverage Years | 2023–2026 |
| 🌍 Source | The Motley Fool |
| 💾 Storage | SQLite + Parquet |
| ✅ Validation | Completed |
| 🧹 Cleaning | Completed |
| 📈 EDA | Completed |

---

# 🧩 Dataset Includes

Each transcript contains:

- 🏢 Company metadata
- 📈 Stock ticker
- 📅 Quarter and fiscal year
- 🗓️ Call date
- 🧹 Clean transcript
- 📰 Article sections
- 🔗 Source URL

---

# 🏗️ Project Architecture + Semantic Intelligence Pipeline

```text
.
├── analysis
│   ├── charts
│   ├── charts_clean
│   ├── gephi
│   ├── reports
│   ├── clean_dataset.py
│   ├── eda.py
│   ├── eda_clean.py
│   ├── export_parquet.py
│   └── validate_dataset.py
│
├── data
│   ├── database
│   │   ├── build_database.py
│   │   ├── transcripts.db
│   │   ├── transcripts_clean.db
│   │   └── transcripts_clean.parquet
│   │
│   └── processed
│       ├── json
│       └── txt
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── data
│   │   └── App.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── src
│   ├── scraper
│   │   ├── discover.py
│   │   ├── bulk_fetch.py
│   │   └── fetcher.py
│   │
│   └── kg
│       └── build_knowledge_graph.py
│
├── scripts
│   ├── analytics
│   ├── graph
│   ├── slurm
│   └── testing
│
├── pyproject.toml
├── uv.lock
└── README.md


🔄 COMPLETE SEMANTIC INTELLIGENCE PIPELINE

discover.py
↓
URL discovery
↓
bulk_fetch.py
↓
Large-scale transcript scraping
↓
transcripts.db
↓
validate_dataset.py
↓
Dataset validation with pandas
↓
clean_dataset.py
↓
Schema normalization
↓
transcripts_clean.db
↓
eda_clean.py
↓
EDA + charts + statistical analysis
↓
export_parquet.py
↓
Parquet generation
↓
Hugging Face dataset publication
↓
Embedding-ready structured dataset
↓
Knowledge graph generation
↓
Semantic propagation analysis
↓
Multi-agent reasoning layer
↓
Financial intelligence dashboard
↓
RAG + semantic retrieval systems
↓
Enterprise AI platform
```

---

# 🧠 Semantic Intelligence Layer

The project evolves beyond traditional sentiment analysis.

Core research focus:

- 🌐 Semantic propagation across economic sectors
- 🔗 Knowledge graph intelligence
- 📡 Signal transmission through supply chains
- 🤖 Multi-agent financial reasoning
- 🧠 AI-powered semantic analysis
- 📈 Real-time financial intelligence dashboards

Example propagation:

```text
AI demand spike
↓
NVIDIA earnings calls
↓
TSMC capacity pressure
↓
Cloud infrastructure expansion
↓
Power grid demand increase
```

The goal is not only to analyze sentiment, but to understand:

- how economic signals spread
- how sectors influence each other
- how supply chain pressure propagates
- how AI agents can reason over financial data
- how semantic relationships emerge over time

---

# 🌐 Knowledge Graph System

The platform generates semantic financial graphs using:

- 🏢 Companies
- 🏭 Economic sectors
- 📡 Semantic signals
- 🔗 Propagation relationships

Generated outputs:

- `.gexf` → Gephi visualization
- `.gpickle` → NetworkX graphs
- `.csv` → Nodes and edges export

Current graph scale:

| Metric | Value |
|---|---|
| 🔹 Nodes | 1,500+ |
| 🔸 Edges | 3,300+ |

The graph layer enables:

- propagation tracking
- semantic clustering
- sector dependency analysis
- anomaly detection
- graph-based AI reasoning

---

# 🖥️ Enterprise Dashboard

The platform includes a modern React + Tailwind enterprise dashboard featuring:

- 🌐 Semantic propagation graph
- 🤖 Multi-agent reasoning stream
- 📈 Sector heatmaps
- ⏳ Temporal propagation timeline
- 🚨 Live alerts and anomalies
- 📡 Financial intelligence panels
- 🔎 Future RAG chat integration

### Frontend Stack

- ⚛️ React
- ⚡ Vite
- 🎨 TailwindCSS
- 🎞️ Framer Motion
- 🌐 React Flow

The dashboard aims to resemble:

- Bloomberg Terminal
- Palantir Foundry
- AI-powered financial intelligence systems

---

# 🧹 Cleaning & Normalization

Raw transcripts originally contained:

- schema.org metadata
- article intro
- takeaways
- summary sections
- glossary sections
- full transcript

The cleaning pipeline separates them into structured columns:

| Column | Description |
|---|---|
| `article_intro` | Introductory article section |
| `takeaways` | Key bullet-point takeaways |
| `summary` | Motley Fool summary |
| `glossary` | Industry glossary |
| `transcript_clean` | Clean earnings call transcript |

This significantly improves:

- 🧠 NLP quality
- 📦 Embedding consistency
- ✂️ Semantic chunking
- 🤖 Downstream ML tasks

---

# 📈 Exploratory Data Analysis (EDA)

The project includes:

- 📊 Transcript length distribution
- 📉 Outlier analysis
- 🏢 Ticker distribution
- 📅 Quarter distribution
- 📈 Company distribution
- 🧹 Raw vs clean comparison
- ⏳ Timeline analysis

Generated charts are stored in:

```text
analysis/charts/
analysis/charts_clean/
analysis/gephi/
```

---

# 💾 Storage Layers

## 📥 Raw Layer

- TXT transcripts
- JSON transcripts

## 🧱 Structured Layer

- SQLite databases

## 🧠 ML / AI Layer

- Parquet datasets
- Knowledge graphs
- Semantic propagation graphs
- Embedding-ready semantic data

---

# ☁️ Hugging Face Integration

The cleaned dataset is designed for publication on Hugging Face for:

- 🔁 Reproducibility
- ☁️ Cloud access
- 👥 Team collaboration
- 🤖 NLP experimentation
- 📚 LLM fine-tuning
- 🔎 Semantic retrieval systems

---

# 🚀 Future Work

Planned improvements:

- 🔄 Incremental scraping pipeline
- 📡 Real-time transcript ingestion
- 🧍 Speaker segmentation
- ✂️ Semantic chunking
- 🧠 Embedding generation
- 🔎 Vector search
- 📚 RAG pipelines
- 🗂️ ChromaDB / vector DB integration
- 🤖 Multi-agent orchestration
- 📈 Financial semantic forecasting
- 🌐 Real-time propagation engine
- ⚡ WebSocket live updates
- 🧠 Autonomous AI reasoning agents

---

# ⚙️ Installation

This project uses `uv` for dependency management.

## Install dependencies

```bash
uv sync
```

## Activate environment

```bash
source .venv/bin/activate
```

---

# ▶️ Usage

## 1️⃣ Discover transcript URLs

```bash
python src/scraper/discover.py
```

## 2️⃣ Scrape transcripts

```bash
python src/scraper/bulk_fetch.py
```

## 3️⃣ Build SQLite database

```bash
python data/database/build_database.py
```

## 4️⃣ Validate dataset

```bash
python analysis/validate_dataset.py
```

## 5️⃣ Clean and normalize dataset

```bash
python analysis/clean_dataset.py
```

## 6️⃣ Run EDA

```bash
python analysis/eda_clean.py
```

## 7️⃣ Export parquet dataset

```bash
python analysis/export_parquet.py
```

## 8️⃣ Build semantic knowledge graph

```bash
python src/kg/build_knowledge_graph.py
```

## 9️⃣ Run frontend dashboard

```bash
cd frontend

npm install

npm run dev
```

---

# 🎯 Project Vision

This project combines:

- 🧱 Data engineering
- 🧠 Semantic intelligence
- 🤖 AI reasoning systems
- 🌐 Knowledge graphs
- 📊 Interactive dashboards
- 🔎 Retrieval systems
- 📡 Economic signal propagation

The long-term vision is to build a real-time financial semantic intelligence platform capable of:

- understanding economic relationships
- tracking semantic propagation
- supporting financial AI agents
- enabling enterprise-level intelligence systems

---

# 👨‍💻 Authors

## Roger Braun

AKA: Rogério Braunschweiger / Rogersurf

- 🇧🇷🇩🇪 German/Brazilian Citizen
- 🇩🇰 Based in Denmark
- 🧠 AI / ML Researcher
- 💻 Software Developer
- 📊 Financial Semantic Intelligence Researcher

## Chenghao Luo

AKA: Soy

- 🇨🇳 Chinese Citizen
- 🎓 Master’s Student at Aalborg University
- 🌐 Semantic Intelligence Platform Contributor

## Suchanya Baiyam

AKA: Ailee

- 🇹🇭 Thai Citizen
- 🎓 Master’s Student at Aalborg University
- 🌐 Semantic Intelligence Platform Contributor