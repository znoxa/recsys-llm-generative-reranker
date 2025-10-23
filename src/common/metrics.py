from prometheus_client import Counter, Histogram, Gauge, start_http_server
import threading

_metrics_started = False
_lock = threading.Lock()

REQS = Counter('req_total', 'Total requests', ['service','route','status'])
LAT  = Histogram('latency_seconds', 'Latency (s)', ['service','route'])
TOK  = Gauge('tokens_used', 'Tokens used', ['service','route'])
COST = Gauge('inference_cost_usd', 'Cost per request (USD)', ['service','route'])

def ensure_metrics(port: int) -> None:
    global _metrics_started
    with _lock:
        if not _metrics_started:
            start_http_server(port)
            _metrics_started = True
