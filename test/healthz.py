import os
from locust import HttpLocust, TaskSet, task, between

SERVICE_HOST_ENV_NAME = "KUBERNETES_SERVICE_HOST"
SERVICE_PORT_ENV_NAME = "KUBERNETES_SERVICE_PORT"
SERVICE_TOKEN_FILENAME = "/var/run/secrets/kubernetes.io/serviceaccount/token"
SERVICE_CERT_FILENAME = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"

def _join_host_port(host, port):
    """Adapted golang's net.JoinHostPort"""
    template = "%s:%s"
    host_requires_bracketing = ':' in host or '%' in host
    if host_requires_bracketing:
        template = "[%s]:%s"
    return template % (host, port)

class HealthZTask(TaskSet):

    kube_token = None
    kube_cert = None
    headers = {}

    #def setup(self):
    #    with open(SERVICE_TOKEN_FILENAME) as f:
    #        self.kube_token = f.read()
    #    self.kube_cert = SERVICE_CERT_FILENAME
    #    self.headers = {
    #        "Authorization": "Bearer {0}".format(self.kube_token)
    #    }

    @task
    def nginxHeartBeat(self):
        self.client.get("/healthz", verify=False)

    #@task
    #def getPodList(self):
    #    self.client.get("/api/v1/pods", verify = self.kube_cert, headers = self.headers)

    #@task
    #def getNodeList(self):
    #    self.client.get("/api/v1/nodes", verify = self.kube_cert, headers = self.headers)


class K8SAgent(HttpLocust):
    task_set = HealthZTask
    wait_time = between(0, 0)

    #def setup(self):
        #self.host = (
        #    "https://" + _join_host_port(os.environ[SERVICE_HOST_ENV_NAME],
        #                                 os.environ[SERVICE_PORT_ENV_NAME]))

