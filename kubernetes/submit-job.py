import jinja2
import argparse
import yaml
import logging
import logging.config
import requests
import time
import os


def setup_logger_config(logger):
    """
    Setup logging configuration.
    """
    if len(logger.handlers) == 0:
        logger.propagate = False
        logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(filename)s:%(lineno)s : %(message)s')
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)


logger = logging.getLogger(__name__)
setup_logger_config(logger)


def load_yaml_config(config_path):
    with open(config_path, "r") as f:
        config_data = yaml.load(f, yaml.SafeLoader)
    return config_data


def read_template(template_path):
    with open(template_path, "r") as f:
        template_data = f.read()
    return template_data


def generate_from_template_dict(template_data, map_table):
    generated_file = jinja2.Template(template_data).render(
        map_table
    )
    return generated_file


def write_generated_file(file_path, content_data):
    with open(file_path, "w+") as fout:
        fout.write(content_data)


def generate_template_file(template_file_path, output_path, map_table):
    template = read_template(template_file_path)
    generated_template = generate_from_template_dict(template, map_table)
    write_generated_file(output_path, generated_template)


def get_token(user, password, url):
    payload = {
        'username': user,
        'password': password,
    }
    r = requests.post("{0}/rest-server/api/v2/authn/basic/login".format(url), data=payload)
    return r.json()['token']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', dest="user", required=True,
                        help="openpai-user")
    parser.add_argument('-p', '--password', dest="password", required=True,
                        help="openpai-password")
    parser.add_argument('-j', '--job-file-template', dest="job", required=True,
                        help="openpai job path")
    parser.add_argument('-n', '--job-name', dest="name", required=True, help="jobname prefix")
    parser.add_argument('-m', '--number', dest="number", required=True,
                        help="openpai job number to start")
    parser.add_argument('-t', '--pai-user', dest="url", required=True, help="pai url")
    args = parser.parse_args()

    job = os.path.expanduser(args.job)
    prefix = args.name
    number = args.number
    user = args.user
    password = args.password
    url = args.url

    token = get_token(user, password, url)
    openpai_headers = {
        "Authorization": "Bearer {0}".format(token),
        "Content-Type": "text/yaml"
    }

    job_template = read_template(job)
    for i in range(number):
        logger.info("Submit job {0}-{1}".format(prefix, i))
        template_data = generate_from_template_dict(job_template, "{0}-{1}".format(prefix, i))
        res = requests.post("{0}/rest-server/api/v2/jobs".format(url), headers=openpai_headers, data=template_data)
        time.sleep(1)

if __name__ == "__main__":
    main()