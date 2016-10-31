# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import logging
import argparse
import yaml
import re

from docker import client

__title__ = 'docker-tasks'
__version__ = '0.1.0'
__author__ = 'Reimund Klain'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Reimund Klain'

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

def main():
    args = get_argparse()
    setup(args)
    with open(args.config) as fd:
        config = yaml.load(fd.read())
    c = client.Client('unix://var/run/docker.sock')
    for container in c.containers():
        app_backup(c, config, container)

def setup(args):
    if args.verbose:
        log.setLevel(logging.DEBUG)

def app_backup(c, config, container):
    cid = container['Id']
    sid = cid[:12]
    image = container['Image']
    names = ', '.join([ n.replace('/', '') for n in container['Names']])
    version = None
    commands = []
    if ':' in image:
        image, version = container['Image'].split(':')

    app = config.get('images').get(image)
    if not app:
        log.info("{}: image: '{}' version: '{}' name: '{}' command: '{}'".format(
            sid, image, version, names, None))
        return

    if version:
        for k in app.keys():
            p = '^%s$' % k.replace('.', '\.').replace('*', '.*')
            log.debug(p)
            match = re.search(p, version)
            if match:
                commands += app.get(k)

    for command in commands:
        cmd = command
        log.debug("{}: image: '{}' version: '{}' names: '{}'".format(sid, image, version, names))
        log.debug("{}: command: '{}'".format(sid, command))
        e = c.exec_create(cid, cmd)
        for o in c.exec_start(e, stream=True):
            for l in o.splitlines():
                log.info('{}: {}'.format(sid, l.decode('utf-8')))


def get_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default="./docker-tasks.yml", help="Config yaml. Default (docker-tasks.yml)")
    parser.add_argument('-v', '--verbose', action='store_true', help='Increate output verbosity')
    return parser.parse_args()

if __name__ == '__main__':
    sys.exit(main())


