# -*- coding: utf-8 -*-

import sys
import logging
import argparse
import yaml
import re

from docker.client import APIClient

__title__ = "docker-tasks"
__version__ = "0.1.0"
__author__ = "Reimund Klain"
__license__ = "BSD"
__copyright__ = "Copyright 2023 - Reimund Klain"

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():
    args = parse_args()
    setup(args)
    with open(args.config) as fd:
        config = yaml.safe_load(fd.read())
    c = APIClient(args.docker_host)
    for container in c.containers():
        execute(c, config, container)


def setup(args):
    if args.verbose:
        log.setLevel(logging.DEBUG)


def execute(c, config, container):
    """
    Execute via docker exec

    :param c: docker client
    :param config: config dict
    :param container: container dict
    :return: None
    """
    cid = container["Id"]
    sid = cid[:12]
    image = container["Image"]
    names = ", ".join([n.replace("/", "") for n in container["Names"]])
    version = None
    commands = []
    if ":" in image:
        image, version = container["Image"].split(":", 1)

    app = config.get("images").get(image)
    if not app:
        log.debug(
            "{}: image: '{}' version: '{}' name: '{}' command: '{}'".format(
                sid, image, version, names, None
            )
        )
        return

    parse_commands(app, version, commands)

    for command in commands:
        cmd = command
        log.debug(
            "{}: image: '{}' version: '{}' names: '{}'".format(
                sid, image, version, names
            )
        )
        log.debug("{}: command: '{}'".format(sid, command))
        e = c.exec_create(cid, cmd)
        for o in c.exec_start(e, stream=True):
            for l in o.splitlines():
                log.info("{}: {}".format(sid, l.decode("utf-8")))


def parse_commands(container, version, commands):
    """
    Parse commands by pattern and versions

    :param container:
    :param version:
    :param commands:
    :return:
    """
    for k in container.keys():
        p = r"^%s$" % k.replace(".", r"\.").replace("*", ".*")
        match = re.search(p, version or "latest")
        if match:
            commands += container.get(k)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        default="./docker-tasks.yml",
        help="Config yaml. Default (docker-tasks.yml)",
    )
    parser.add_argument(
        "--docker-host",
        default="unix://var/run/docker.sock",
        help="Docker host. Default (unix://var/run/docker.sock)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase output verbosity"
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
