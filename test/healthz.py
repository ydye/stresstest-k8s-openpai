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
        template_data = f.read()

    return template_data

def generate_from_template_dict(template_data, jobname):

    generated_file = jinja2.Template(template_data).render(
        {'jobname': jobname}
    )

    return generated_file


with open(SERVICE_TOKEN_FILENAME) as f:
    kube_token = f.read()
kube_cert = SERVICE_CERT_FILENAME
k8s_headers = {
            "Authorization": "Bearer {0}".format(kube_token)
}
kube_url = "https://{0}".format(_join_host_port(os.environ[SERVICE_HOST_ENV_NAME], os.environ[SERVICE_PORT_ENV_NAME]))
pai_token = os.environ["PAI_TOKEN"]
job_template = read_template("/mnt/locust/test-job.yml")
id = 0

class HealthZTask(TaskSet):
    '''
    @task(1)
    def submitjob(self):
        hostname = os.environ['MY_POD_NAME']
        jobname = "stresstest-{0}-{1}".format(hostname, self.id)
        self.id = self.id + 1

        template_data = generate_from_template_dict(self.job_template, jobname)


        openpai_headers = {
            "Authorization": "Bearer {0}".format(self.pai_token),
            "Content-Type": "text/yaml"
        }

        self.client.post(
            "/rest-server/api/v2/jobs",
            headers=openpai_headers,
            data=template_data
        )
    '''

    @task(10)
    def listjoball(self):
        openpai_headers = {
            "Authorization": "Bearer {0}".format(pai_token),
        }
        self.client.get(
            "/rest-server/api/v2/jobs",
            headers=openpai_headers
        )

    '''
    @task(10)
    def getPodList(self):
        self.client.get(self.kube_url + "/api/v1/nodes", verify = self.kube_cert, headers = self.k8s_headers)
    '''

class K8SAgent(HttpLocust):
    task_set = HealthZTask
    wait_time = between(10, 10)

