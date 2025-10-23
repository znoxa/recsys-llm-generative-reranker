.PHONY: fmt lint test run-all eval

fmt:
	black src tools eval

lint:
	flake8 src tools eval || true

test:
	pytest -q || true

run-all:
	python src/candidate/service.py --port 8081 & 	python src/reranker_llm/service.py --port 8083 & 	python src/gateway/service.py --port 8080 & 	wait

eval:
	python eval/evaluate_offline.py --data eval/data/synthetic_interactions.jsonl
