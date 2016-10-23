# -*- coding: utf-8 -*-

__title__ = 'docker-backup'
__version__ = '0.1.0'
__author__ = 'Reimund Klain'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Reimund Klain'

import sys
import logging
import datetime as dt
from collections import defaultdict

from docker import client

from pprint import pprint

import yaml

from . import dbs

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CONFIG="""

images:
    ubuntu:
      '14.04':
        - ps aux

    postgres:
      '9.4':
        - /bin/sh -c "pg_dump -U postgres postgres > /var/lib/postgresql/data/db_backup_$(date +%u).sql\"

"""

def main():
    config = yaml.load(CONFIG)
    c = client.Client('unix://var/run/docker.sock')
    for container in c.containers():
        log.info("Handle container id: '{}' image: '{}'".format(container['Id'], container['Image']))
        log.debug(pprint(container))
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
        log.warning("No commoand found for image: '{}'".format(image))
        return
    commands = app.get(version)
    if not commands:
        log.warning("No command found for version: '{}'".format(version))
        return

    for command in commands:
        cmd = command
        e = c.exec_create(cid, cmd)
        for o in c.exec_start(e, stream=True):
            for l in o.splitlines():
                log.debug(l)

if __name__ == '__main__':
    sys.exit(main())


