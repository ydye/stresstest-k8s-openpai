import jinja2
import argparse
import yaml
import logging
import logging.config
import requests
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', dest="user", required=True,
                        help="openpai-user")
    parser.add_argument('-p', '--password', dest="password", required=True,
                        help="openpai-password")
    parser.add_argument('-j', '--job-file', dest="job", required=True,
                        help="openpai job path")
    parser.add_argument('-m', '--number', dest="number", required=True,
                        help="openpai job number to start")
    args = parser.parse_args()
    output_path = os.path.expanduser(args.output)

    environment = {
        'cfg': load_yaml_config(args.configuration),
    }
    map_table = {
        "env": environment
    }
    generate_template_file(
        "kubernetes/locust-master.yml.j2",
        "{0}/locust-master.yml".format(output_path),
        map_table
    )
    generate_template_file(
        "kubernetes/locust-slave.yml.j2",
        "{0}/locust-slave.yml".format(output_path),
        map_table
    )


if __name__ == "__main__":
    main()