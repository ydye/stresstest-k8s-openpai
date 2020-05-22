import os
import requests
import yaml
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

    def setup(self):
        with open(SERVICE_TOKEN_FILENAME) as f:
            self.kube_token = f.read()
        self.kube_cert = SERVICE_CERT_FILENAME
        self.headers = {
            "Authorization": "Bearer {0}".format(self.kube_token)
        }

        self.pai_user = os.environ['PAI_USER']
        self.pai_password = os.environ['PAI_PASSWORD']
        self.pai_restserver = os.environ['TARGET_URL']

        payload = {
            'username': self.pai_user,
            'password': self.pai_password,
        }
        r = requests.post("{0}/rest-server/api/v2/authn/basic/login".format(self.pai_restserver), data = payload)
        self.pai_token = r.json()['token']


    @task(1)
    def submitjob(self):
        headers = {
            "Authorization": "Bearer {0}".format(self.pai_token),
            "Content-Type": "text/yaml"
        }

        self.client.post(
            "/rest-server/api/v2/job",
            headers=headers
        )

    #@task
    #def getPodList(self):
    #    self.client.get("/api/v1/pods", verify = self.kube_cert, headers = self.headers)

    #@task
    #def getNodeList(self):
    #    self.client.get("/api/v1/nodes", verify = self.kube_cert, headers = self.headers)


class K8SAgent(HttpLocust):
    task_set = HealthZTask
    wait_time = between(1, 10)

