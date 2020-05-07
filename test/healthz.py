from locust import HttpLocust, TaskSet, task, between

class HealthZTask(TaskSet):
    @task
    def nginxHeartBeat(self):
       self.client.get("/healthz", verify=False)

    @task
    def getPodList(self):
        None

    @task
    def getNodeList(self):
        None

class K8SAgent(HttpLocust):
    task_set = HealthZTask
    wait_time = between(10, 10)