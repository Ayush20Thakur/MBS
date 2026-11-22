from locust import HttpUser, task, between
import uuid

class PaymentClientUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def health_probe(self):
        self.client.get("/api/v1/health")

    @task(1)
    def fetch_metrics(self):
        self.client.get("/api/v1/metrics")
