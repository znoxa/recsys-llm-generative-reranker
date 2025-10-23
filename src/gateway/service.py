import argparse, time
from fastapi import FastAPI
from pydantic import BaseModel
import httpx, orjson
from loguru import logger
from src.common.config import Settings
from src.common.metrics import ensure_metrics, REQS, LAT

class RecRequest(BaseModel):
    user_id: str
    query: str = ""
    history: str = ""
    topk: int = 10

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

app = FastAPI(default_response_class=None)
CFG = None
CLIENT = httpx.AsyncClient(timeout=5.0)

@app.post("/recommend")
async def recommend(req: RecRequest):
    REQS.labels('gateway','recommend','in').inc()
    t0 = time.time()
    # 1) get candidates
    c = await CLIENT.post(CFG.get('services.candidate_url') + "/candidates", json={'user_id': req.user_id, 'query': req.query, 'topk': 200})
    # 2) LLM rerank
    r = await CLIENT.post(CFG.get('services.reranker_url') + "/rerank", json={
        'user_id': req.user_id,
        'query': req.query,
        'history': req.history,
        'candidates': c.json(),
        'topk': req.topk
    })
    LAT.labels('gateway','recommend').observe(time.time()-t0)
    REQS.labels('gateway','recommend','ok').inc()
    return {'user_id': req.user_id, 'recommendations': r.json()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='configs/dev.yaml')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    global CFG
    CFG = Settings.from_file(args.config)
    ensure_metrics(CFG.get('observability.prometheus_port', 9100))
    logger.info("Gateway on {}", args.port)
    import uvicorn
    uvicorn.run("src.gateway.service:app", host="0.0.0.0", port=args.port, reload=False)

if __name__ == "__main__":
    main()
