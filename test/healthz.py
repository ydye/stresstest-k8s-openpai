import os
import requests
import socket
import yaml
import jinja2
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

def read_template(template_path):

    with open(template_path, "r") as f:
        template_data = f.read().decode('utf-8')

    return template_data

def generate_from_template_dict(template_data, jobname):

    generated_file = jinja2.Template(template_data).render(
        {'jobname': jobname}
    )

    return generated_file

class HealthZTask(TaskSet):

    kube_token = None
    kube_cert = None
    id = 0

    def setup(self):
        with open(SERVICE_TOKEN_FILENAME) as f:
            self.kube_token = f.read()
        self.kube_cert = SERVICE_CERT_FILENAME
        self.k8s_headers = {
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

        self.job_template = read_template("/mnt/locust/test-job.yml")

    @task(1)
    def submitjob(self):
        hostname = socket.gethostbyname()
        jobname = "stresstest-{0}-{1}".format(hostname, self.id)
        self.id = id + 1

        template_data = generate_from_template_dict(self.job_template, jobname)


        openpai_headers = {
            "Authorization": "Bearer {0}".format(self.pai_token),
            "Content-Type": "text/yaml"
        }

        self.client.post(
            "/rest-server/api/v2/job",
            headers=openpai_headers,
            data=template_data
        )


    @task(1)
    def listjoball(self):
        openpai_headers = {
            "Authorization": "Bearer {0}".format(self.pai_token),
        }
        self.client.get(
            "/rest-server/api/v2/job",
            headers=openpai_headers
        )


    @task(1)
    def listjoball(self):
        openpai_headers = {
            "Authorization": "Bearer {0}".format(self.pai_token),
        }
        self.client.get(
            "/rest-server/api/v2/job",
            headers=openpai_headers
        )

    #@task(1)
    #def getPodList(self):
    #    self.client.get("/api/v1/pods", verify = self.kube_cert, headers = self.k8s_headers)

    #@task
    #def getNodeList(self):
    #    self.client.get("/api/v1/nodes", verify = self.kube_cert, headers = self.headers)


class K8SAgent(HttpLocust):
    task_set = HealthZTask
    wait_time = between(60, 60)

