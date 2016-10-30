# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

__title__ = 'docker-tasks'
__version__ = '0.1.0'
__author__ = 'Reimund Klain'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Reimund Klain'

import sys
import logging
import argparse

from docker import client
import yaml

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def main():
    args = get_argparse()
    with open(args.config) as fd:
        config = yaml.load(fd.read())
    c = client.Client('unix://var/run/docker.sock')
    for container in c.containers():
        log.info("Handle container id: '{}' image: '{}'".format(container['Id'], container['Image']))
        #log.debug(pprint(container))
        app_backup(c, config, container)


def app_backup(c, config, container):
    cid = container['Id']
    image = container['Image']
    name = container['Names'][0].replace('/', '')
    version = None
    if ':' in image:
        image, version = container['Image'].split(':')

    app = config.get('images').get(image)
    if not app:
        log.warning("No task found for image: '{}'".format(image))
        return
    commands = app.get(version)
    if not commands:
        log.warning("No task found for version: '{}'".format(version))
        return

    for command in commands:
        cmd = command
        e = c.exec_create(cid, cmd)
        for o in c.exec_start(e, stream=True):
            for l in o.splitlines():
                log.debug(l)


def get_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default="./docker-tasks.yml", help="Config yaml. Default (docker-tasks.yml)")
    return parser.parse_args()

if __name__ == '__main__':
    sys.exit(main())


