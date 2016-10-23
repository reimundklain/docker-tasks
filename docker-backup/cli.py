# -*- coding: utf-8 -*-

__title__ = 'docker-backup'
__version__ = '0.1.0'
__author__ = 'Reimund Klain'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Reimund Klain'

import sys
from docker import client

def main():

    c = client.Client('unix://var/run/docker.sock')
    print(c.containers())


if __name__ == '__main__':
    main()


