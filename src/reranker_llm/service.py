import argparse, time, json
from fastapi import FastAPI
from pydantic import BaseModel
import httpx, yaml
from loguru import logger
from src.common.metrics import ensure_metrics, REQS, LAT, TOK, COST
from .prompts import build_prompt
from .adapters.mock import MockLLM

app = FastAPI()

CFG = None
CLIENT = httpx.AsyncClient(timeout=5.0)
LLM = None
PROMPTS = None

class ReRankReq(BaseModel):
    user_id: str
    query: str = ""
    history: str = ""
    candidates: list
    topk: int = 10

@app.post("/rerank")
async def rerank(req: ReRankReq):
    REQS.labels('reranker-llm','rerank','in').inc()
    t0 = time.time()
    prompt = build_prompt(PROMPTS['system_prompt'], PROMPTS['user_template'], req.user_id, req.query, req.history, req.candidates, req.topk)
    # Simulated token usage (length / 4 rough heuristic)
    tok_in = max(16, len(prompt)//4)
    generated = LLM.generate(prompt, stop=PROMPTS.get('stop_words',[]))
    tok_out = max(8, len(generated)//4)
    TOK.labels('reranker-llm','rerank').set(tok_in + tok_out)
    # Simulated cost
    cost = (tok_in + tok_out)/1000.0 * 0.002  # $0.002 / 1K tok mock
    COST.labels('reranker-llm','rerank').set(cost)
    try:
        parsed = json.loads(generated)
    except Exception:
        parsed = []
    # Merge with original metadata
    meta = {c['item_id']: c for c in req.candidates}
    out = []
    for r in parsed[: req.topk]:
        it = meta.get(r['item_id'])
        if it:
            it2 = {**it, "score": r.get("score", 0.0), "rationale": r.get("rationale","")}
            out.append(it2)
    LAT.labels('reranker-llm','rerank').observe(time.time()-t0)
    REQS.labels('reranker-llm','rerank','ok').inc()
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8083)
    parser.add_argument('--config', default='configs/dev.yaml')
    parser.add_argument('--prompts', default='configs/prompts.yaml')
    args = parser.parse_args()
    global CFG, LLM, PROMPTS
    with open(args.config, 'r', encoding='utf-8') as f:
        CFG = yaml.safe_load(f)
    with open(args.prompts, 'r', encoding='utf-8') as f:
        PROMPTS = yaml.safe_load(f)
    LLM = MockLLM(max_tokens=CFG.get('llm',{}).get('max_tokens',128))
    ensure_metrics(9303)
    logger.info("LLM reranker on {}", args.port)
    import uvicorn
    uvicorn.run("src.reranker_llm.service:app", host="0.0.0.0", port=args.port, reload=False)

if __name__ == "__main__":
    main()
