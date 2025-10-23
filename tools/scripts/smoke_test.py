import requests, time, json

def main():
    r = requests.post("http://localhost:8080/recommend", json={"user_id":"u1","query":"romance","topk":5})
    print("Status:", r.status_code)
    print("Body:", json.dumps(r.json()[:1] if isinstance(r.json(), list) else r.json(), indent=2))

if __name__ == "__main__":
    main()
