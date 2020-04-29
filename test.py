import argparse
from locust import HttpLocust, TaskSet, between

class HealthZTask(TaskSet):
    @task
    def nginxHeartBeat(self):
        None

class StressTest(HttpLocust):
    task_set = HealthZTask



