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

from . import dbs

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

APPS = dict(
    ubuntu=dict(
        versions={
        '14.04': [dict(cmd='ps aux')]
        }
    ),
    postgres=dict(
        versions={
        '9.4': [
            dict(
                cmd='pg_dump -U postgres postgres',
                output= True,

            ),
            dict(
                cmd='/bin/sh -c \"pg_dump -U postgres postgres > /var/lib/postgresql/data/db_backup_$(date +%u).sql\"'
            )
        ],
        }
    )
)


def main():

    c = client.Client('unix://var/run/docker.sock')
    for container in c.containers():
        log.info("Handle container id: '{}' image: '{}'".format(container['Id'], container['Image']))
        log.debug(pprint(container))
        app_backup(c, container)


def app_backup(c, container):
    cid = container['Id']
    image = container['Image']
    name = container['Names'][0].replace('/', '')
    version = None
    if ':' in image:
        image, version = container['Image'].split(':')

    app = APPS.get(image)
    if not app:
        log.warning("No commoand found for image: '{}'".format(image))
        return
    commands = app.get('versions').get(version)
    if not commands:
        log.warning("No commoand found for version: '{}'".format(version))
        return

    for command in commands:
        cmd = command.get('cmd')
        is_stream = command.get('is_stream', False)
        e = c.exec_create(cid, cmd)

        fd = None
        if is_stream:
            fd = open('backup/{}.sql'.format(name), 'wb')
        try:
            for o in c.exec_start(e, stream=True):
                if is_stream: fd.write(o)
                for l in o.splitlines():
                    log.debug(l)
        finally:
            if is_stream: fd.close()

if __name__ == '__main__':
    sys.exit(main())


