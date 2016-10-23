# -*- coding: utf-8 -*-

__title__ = 'docker-backup'
__version__ = '0.1.0'
__author__ = 'Reimund Klain'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Reimund Klain'

import sys
import logging
from collections import defaultdict

from docker import client

from pprint import pprint

from . import dbs

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

APPS = dict(
    ubuntu={
        '14.04': 'ps aux'
    },
    postgres={
        '9.4': "pg_dump -U postgres postgres",
        'latest': "pg_dump -U postgres postgres",
    }

)


def main():

    c = client.Client('unix://var/run/docker.sock')
    for container in c.containers():
        log.debug("Handle container id: '{}' image: '{}'".format(container['Id'], container['Image']))
        app_backup(c, container)


def app_backup(c, container):
    cid = container['Id']
    image = container['Image']
    version = None
    if ':' in image:
        image, version = container['Image'].split(':')

    app = APPS.get(image)
    if not app:
        log.warning("No commoand found for image: '{}'".format(image))
        return
    command = app.get(version)
    if not command:
        log.warning("No commoand found for version: '{}'".format(version))
        return

    e = c.exec_create(cid, command)
    for o in c.exec_start(e, stream=True):
        for l in o.splitlines():
            print(l)



if __name__ == '__main__':
    sys.exit(main())


