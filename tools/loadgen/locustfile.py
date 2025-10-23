from locust import HttpUser, task, between
import random, time

class LLMRRUser(HttpUser):
    wait_time = between(0.01, 0.2)

    @task
    def recommend(self):
        uid = f"u{random.randint(1, 10_000_000)}"
        q = random.choice(["cozy mystery","sci-fi","romance","note-taking app","budgeting app"])
        payload = {"user_id": uid, "query": q, "topk": random.choice([10,20,50])}
        self.client.post("/recommend", json=payload, name="recommend")
