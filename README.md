# earnings-call-analysis

earnings-call-analysis/
│
data/
│
├── discovered/
│   └── urls.jsonl
│
├── raw/
│   ├── html/
│   └── json/
│
├── processed/
│   ├── txt/
│   ├── parquet/
│   └── cleaned/
│
├── database/
│   └── transcripts.db
│
└── logs/
│
├── src/
│   ├── scraper/
│   │   ├── discover.py
│   │   ├── fetcher.py
│   │   └── parser.py
│   │
│   ├── database/
│   │   └── db.py
│   │
│   ├── models/
│   │   └── transcript.py
│   │
│   └── utils/
│       └── helpers.py
│
├── main.py
├── pyproject.toml
└── .env

discover.py
↓
coletar ALL transcript URLs
↓
save urls.json
↓
fetcher.py
↓
extract structured data
↓
save raw json
↓
cleaner.py
↓
normalize transcript
↓
database.py
↓
persist