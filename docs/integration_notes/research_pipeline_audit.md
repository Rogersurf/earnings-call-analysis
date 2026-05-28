# Research Pipeline Audit

## Goal

Absorb the strongest retrieval and ingestion engineering components from the Soy repository into the current semantic intelligence platform architecture.

Main repository remains the source of truth.

The integration strategy prioritizes architectural consistency, semantic governance, modular retrieval infrastructure, and frontend compatibility instead of directly merging repositories.

---

## Current Focus

### Retrieval
- chunk discipline
- hybrid retrieval
- reranking
- graph-aware retrieval
- metadata rigor
- semantic layer retrieval

### Semantic Governance
- multi-layer indexing
- speaker-aware retrieval
- semantic collection separation
- discourse-aware retrieval
- retrieval governance

### Graph Expansion
- semantic propagation graphs
- cross-company retrieval
- graph node generation
- graph edge generation
- semantic neighborhood exploration

### Platform Integration
- FastAPI orchestration
- frontend/backend integration
- semantic exploration UI
- graph-aware platform services

---

## Reviewed Files

### build_chroma_rag_index.py
STATUS: reviewed
ACTION: adapted
DESTINATION: backend/app/research_pipeline/retrieval/index_builder.py

### retrieve_chroma_rag_evidence.py
STATUS: reviewed
ACTION: adapted
DESTINATION: backend/app/research_pipeline/retrieval/retriever.py

### extract_llm_agents_csv_vllm.py
STATUS: reviewed
ACTION: partially adapted
DESTINATION: backend/app/research_pipeline/agents/

### seekingalpha.py
STATUS: reviewed
ACTION: partially adapted
DESTINATION: backend/app/research_pipeline/ingestion/

---

## New Integrated Files

### index_builder.py
STATUS: integrated
PURPOSE:
- Chroma indexing
- multi-collection indexing
- semantic document persistence
- embedding generation

### retriever.py
STATUS: integrated
PURPOSE:
- semantic retrieval
- Chroma querying
- hybrid retrieval pipeline
- reranked retrieval orchestration

### reranker.py
STATUS: integrated
PURPOSE:
- financial reranking
- semantic score weighting
- retrieval refinement
- semantic layer prioritization

### schema_adapter.py
STATUS: integrated
PURPOSE:
- semantic routing
- multi-collection governance
- speaker-aware document routing
- metadata normalization

### graph_expander.py
STATUS: integrated
PURPOSE:
- semantic propagation graph generation
- node expansion
- graph edge construction
- cross-company semantic linking

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

### research_service.py
STATUS: integrated
PURPOSE:
- orchestration layer
- retrieval service abstraction
- graph service orchestration
- frontend/backend bridge

### research.py
STATUS: integrated
PURPOSE:
- FastAPI semantic retrieval routes
- graph expansion routes
- research API exposure

### researchService.js
STATUS: integrated
PURPOSE:
- frontend/backend API communication
- semantic retrieval requests
- graph retrieval requests

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
- FastAPI integration
- frontend/backend integration
- semantic retrieval API exposure
- graph retrieval API exposure
- frontend semantic query integration
- local network deployment support

---

## Current Findings

### Retrieval
- retrieval pipeline fully operational
- semantic reranking operational
- semantic layer weighting operational
- cross-company retrieval operational

### Graph Expansion
- semantic graph expansion operational
- graph edge generation operational
- graph node export operational
- self-loop graph issue resolved

### Semantic Governance
- multi-layer retrieval functioning correctly
- speaker-aware retrieval functioning
- metadata alignment partially noisy in analyst parsing
- semantic routing architecture stable

### Frontend Integration
- frontend successfully connected to research backend
- semantic query orchestration operational
- graph-ready UI architecture confirmed
- retrieval visualization pipeline operational

### Current Limitations
- retrieval quality still limited by general-purpose embeddings
- graph currently represents semantic similarity rather than economic causality
- speaker metadata still partially noisy
- graph visualization still requires refinement and hierarchy improvements
- BM25 and query expansion not yet integrated

---

## Current Architecture

earnings transcripts
→ discourse normalization
→ semantic routing
→ governed indexing
→ hybrid retrieval
→ reranking
→ graph expansion
→ semantic propagation exploration
→ FastAPI orchestration
→ frontend semantic visualization

---

## Integration Strategy

### Repository Governance
- main repository remains the canonical platform
- Soy repository acts as research feature source
- integration occurs through modular adaptation, not repository fusion
- architectural consistency prioritized over direct code migration

### Engineering Strategy
- preserve platform architecture
- preserve frontend separation of concerns
- integrate retrieval research incrementally
- avoid monolithic experimental merges
- maintain semantic governance principles

---

## Next Step

### Immediate Priority
- SemanticGraph.jsx integration
- live graph rendering
- graph node interaction
- retrieval-to-graph synchronization
- UI hierarchy refinement

### Retrieval Improvements
- financial embeddings
- hybrid BM25 retrieval
- query expansion
- LLM reranking
- retrieval explainability

### Graph Improvements
- sector overlap edges
- supplier relationship edges
- temporal propagation
- economic dependency weighting
- semantic community detection

### Future Platform Direction
- semantic intelligence terminal
- interactive propagation exploration
- lightweight agent orchestration
- semantic signal tracking
- graph-aware semantic reasoning