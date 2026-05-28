# Research Pipeline Audit

## Goal

Absorb the strongest retrieval and ingestion engineering components from the Soy repository into the current semantic intelligence platform architecture.

Main repository remains the source of truth.

---

## Current Focus

### Retrieval
- chunk discipline
- hybrid retrieval
- reranking
- graph-aware retrieval
- metadata rigor

### Semantic Governance
- multi-layer indexing
- speaker-aware retrieval
- semantic collection separation
- discourse-aware retrieval

### Graph Expansion
- semantic propagation graphs
- cross-company retrieval
- graph node generation
- graph edge generation

---

## Reviewed Files

### build_chroma_rag_index.py
STATUS: reviewed
ACTION: adapt
DESTINATION: backend/app/research_pipeline/retrieval/index_builder.py

### retrieve_chroma_rag_evidence.py
STATUS: reviewed
ACTION: adapt
DESTINATION: backend/app/research_pipeline/retrieval/retriever.py

### extract_llm_agents_csv_vllm.py
STATUS: reviewed
ACTION: partial adapt
DESTINATION: backend/app/research_pipeline/agents/

### seekingalpha.py
STATUS: reviewed
ACTION: partial adapt
DESTINATION: backend/app/research_pipeline/ingestion/

---

## New Integrated Files

### schema_adapter.py
STATUS: integrated
PURPOSE:
- semantic routing
- multi-collection governance
- speaker-aware document routing

### reranker.py
STATUS: integrated
PURPOSE:
- financial reranking
- semantic score weighting
- retrieval refinement

### graph_expander.py
STATUS: integrated
PURPOSE:
- semantic propagation graph generation
- node expansion
- graph edge construction

### speaker_parser.py
STATUS: integrated
PURPOSE:
- speaker normalization
- discourse metadata extraction
- speaker type classification

### discourse_cleaner.py
STATUS: integrated
PURPOSE:
- noisy speaker cleanup
- moderator leakage reduction
- discourse structure cleanup

---

## Current Status

### Completed
- semantic multi-collection indexing
- Chroma integration
- governed retrieval architecture
- hybrid retrieval pipeline
- reranking layer
- graph-aware retrieval
- semantic propagation graph generation
- speaker-aware retrieval
- discourse-aware ingestion
- semantic routing architecture

### Current Findings
- retrieval pipeline fully operational
- semantic graph expansion operational
- cross-company retrieval operational
- speaker metadata still partially noisy
- retrieval quality limited by general-purpose embeddings
- current graph is semantic similarity based, not economic causality based

### Current Architecture

ingestion
→ discourse normalization
→ semantic routing
→ governed indexing
→ hybrid retrieval
→ reranking
→ graph expansion
→ semantic propagation exploration

---

## Next Step

### Backend Integration
- research_service.py
- FastAPI routes
- frontend integration

### Future Retrieval Improvements
- query expansion
- financial embeddings
- hybrid BM25 retrieval
- LLM reranking

### Future Graph Improvements
- sector overlap edges
- supplier relationship edges
- temporal propagation
- economic dependency weighting