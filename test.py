from locust import HttpLocust, TaskSet

class HealthZTask(TaskSet):
    @task
    def nginxHeartBeat(self):
       self.client.get("/healthz", catch_response=True)

class K8SAgent(HttpLocust):
    task_set = HealthZTask
    wait_time = 10