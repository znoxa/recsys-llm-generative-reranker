# Leveraging LLMs as Generative Re‑Rankers for Recommendation Inference

**Short description:** A reference implementation of **LLM‑as‑Re‑Ranker (LLM‑RR)** for recommendation inference. It includes a modular serving stack (gateway → candidate gen → **LLM generative re‑ranker**), prompt libraries, **KV‑cache pooling**, **budget/cost controllers**, fallback **neural/linear re‑rankers**, offline evaluation harness (NDCG/MRR/CTR‑lift), and deployment examples.

> The default path runs locally with light mocks; adapters for hosted LLMs (OpenAI, Bedrock, Azure, vLLM, TGI) are provided as stubs to plug into your infra.

---

## Features
- **Prompted Generative Re‑Ranking**: converts user + item facts into instruction prompts to produce **scored rationales** and ranking.
- **Latency/Cost Controls**: dynamic **token budgets**, early‑exit, stop‑word halting, and **top‑K truncation** before LLM.
- **KV‑Cache Pooling**: reuse system/role prefixes across requests (simulated pool API).
- **Safety Filters**: simple PII/off‑policy guard before/after LLM calls.
- **Fallback Cascade**: LLM‑RR → distilled cross‑encoder → linear scorer when SLO or spend is exceeded.
- **A/B, Shadow & Canary**: header‑ and hash‑based experiment routing.
- **Observability**: Prometheus metrics + structured rationale logging for audits.
- **Offline Eval**: synthetic dataset + metrics (NDCG@K, MRR, MAP, pairwise accuracy) and **cost/latency accounting**.

---

## Quick Start (local mock)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run services in separate shells (or `make run-all`)
python src/gateway/service.py --port 8080
python src/candidate/service.py --port 8081
python src/reranker_llm/service.py --port 8083  # mock LLM by default

# Test
curl -s -X POST "http://localhost:8080/recommend" -H "Content-Type: application/json"   -d '{"user_id":"u42","query":"cozy mystery ebooks","topk":10}' | jq
```

**To integrate a real LLM**, implement an adapter in `src/reranker_llm/adapters/` (OpenAI/Bedrock/vLLM/TGI). The default adapter is a cheap heuristic mock for reproducibility.

---

## Layout
```
.
├── README.md
├── LICENSE
├── Makefile
├── pyproject.toml
├── requirements.txt
├── configs/
│   ├── dev.yaml
│   ├── prod.yaml
│   └── prompts.yaml
├── src/
│   ├── common/...
│   ├── gateway/...
│   ├── candidate/...
│   └── reranker_llm/...
├── docs/
│   ├── method.md
│   ├── prompts-and-templates.md
│   ├── latency-and-cost.md
│   ├── eval.md
│   └── security-and-safety.md
├── eval/
│   ├── data/synthetic_interactions.jsonl
│   └── evaluate_offline.py
├── tools/
│   ├── loadgen/locustfile.py
│   └── scripts/smoke_test.py
├── deploy/
│   ├── docker/Dockerfile.*
│   └── k8s/*.yaml
└── .github/workflows/ci.yml
```
See `docs/method.md` and `docs/latency-and-cost.md` for details.
