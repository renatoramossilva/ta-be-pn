from locust import HttpUser, task, between

class LoadTest(HttpUser):
    host = "http://localhost:8000"

    wait_time = between(1, 5)

    @task
    def get_coverage(self):
        self.client.get("/coverage?address=42+rue+papernest+75011+Paris")
