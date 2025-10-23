import json, argparse, random, math
from pathlib import Path

def ndcg_at_k(ranklist, gold, k=10):
    dcg=0.0
    for i,item in enumerate(ranklist[:k], start=1):
        rel=1.0 if item in gold else 0.0
        dcg += (2**rel -1)/math.log2(i+1)
    idcg = sum((2**1 -1)/math.log2(i+1) for i in range(1, min(k,len(gold))+1))
    return dcg/(idcg or 1.0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    args = ap.parse_args()
    ndcgs = []
    with open(args.data, "r", encoding="utf-8") as f:
        for line in f:
            ex = json.loads(line)
            # Fake ranking: positives near the top
            pool = ex["positives"] + ex["negatives"]
            random.shuffle(pool)
            rank = pool  # placeholder
            ndcgs.append(ndcg_at_k(rank, set(ex["positives"]), k=5))
    print({"NDCG@5": round(sum(ndcgs)/len(ndcgs),4), "n": len(ndcgs)})

if __name__ == "__main__":
    main()
