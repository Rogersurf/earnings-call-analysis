# Earnings Call Analysis

A data engineering and NLP-oriented project focused on scraping, cleaning, validating, and structuring earnings call transcripts from The Motley Fool.

The project builds a reproducible pipeline for:
- transcript discovery
- large-scale scraping
- data normalization
- validation
- exploratory data analysis (EDA)
- parquet export
- cloud dataset publishing

The final goal is to provide a clean and structured earnings call dataset ready for:
- NLP
- LLMs
- RAG systems
- semantic search
- embeddings
- sentiment analysis
- financial analytics


---

# Dataset Overview

Current dataset statistics:

| Metric | Value |
|---|---|
| Total transcripts | 9,069 |
| Unique tickers | 2,944 |
| Coverage years | 2023–2026 |
| Dataset type | Earnings call transcripts |
| Source | The Motley Fool |
| Storage formats | SQLite + Parquet |
| Validation | Completed |
| Cleaning | Completed |
| EDA | Completed |

The dataset includes:
- company metadata
- ticker
- quarter
- earnings year
- call date
- cleaned transcript
- article sections
- source URL


---

# Project Structure

```text
.
├── analysis
│   ├── charts
│   ├── charts_clean
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
├── src
│   └── scraper
│       ├── discover.py
│       ├── bulk_fetch.py
│       └── fetcher.py
│
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md

# Data Pipeline

discover.py
↓
collect transcript URLs
↓
bulk_fetch.py
↓
scrape transcripts
↓
transcripts.db
↓
validate_dataset.py
↓
data validation with pandas
↓
clean_dataset.py
↓
schema normalization
↓
transcripts_clean.db
↓
eda_clean.py
↓
EDA + statistics + charts
↓
export_parquet.py
↓
transcripts_clean.parquet
↓
Hugging Face dataset

# Installation

This project uses uv for dependency management.

Install dependencies: uv sync
Activate environment: source .venv/bin/activate

# Usage
1. Discover transcript URLs
python src/scraper/discover.py
2. Scrape transcripts
python src/scraper/bulk_fetch.py
3. Build SQLite database
python data/database/build_database.py
4. Validate dataset
python analysis/validate_dataset.py
5. Clean and normalize dataset
python analysis/clean_dataset.py
6. Run EDA
python analysis/eda_clean.py
7. Export parquet dataset
python analysis/export_parquet.py

Cleaning and Normalization

The raw transcript field originally contained:

schema.org metadata
article intro
takeaways
summary sections
glossary sections
full transcript

The cleaning pipeline separates these into structured columns:

Column	Description
article_intro	Introductory article section
takeaways	Key bullet-point takeaways
summary	Motley Fool summary
glossary	Industry glossary
transcript_clean	Clean earnings call transcript

This significantly improves:

NLP quality
embedding consistency
semantic chunking
downstream ML tasks
Exploratory Data Analysis (EDA)

The project includes:

transcript length distribution
outlier analysis
ticker distribution
quarter distribution
company distribution
raw vs clean comparison
timeline analysis

Charts are saved in:

analysis/charts/
analysis/charts_clean/
Storage Layers
Raw Layer
TXT transcripts
JSON transcripts
Structured Layer
SQLite databases
ML/Analytics Layer
Parquet dataset
Hugging Face Dataset

The cleaned parquet dataset is intended for publication on Hugging Face datasets for:

reproducibility
cloud access
team collaboration
downstream NLP applications
Future Work

Planned improvements:

incremental scraping pipeline
automatic dataset updates
speaker segmentation
transcript chunking
embedding generation
semantic search
RAG pipelines
vector database integration
sentiment analysis
financial NLP benchmarking
Notes

The project is intentionally separated into:

data engineering pipeline
downstream application layer

This allows:

reusable datasets
cleaner architecture
easier collaboration
independent ML applications
Author

Roger Braun (AKA: Rogério Braunschweiger, Rogersurf)

Earnings Calls
        ↓
Corpus Statistics
        ↓
Entity Extraction
        ↓
SBERT Embeddings
        ↓
Vector Database
        ↓
Knowledge Graph
        ↓
Propagation Engine
        ↓
FinBERT Analysis
        ↓
LLM Reasoning Layer
        ↓
Dashboard / Multi-Agent