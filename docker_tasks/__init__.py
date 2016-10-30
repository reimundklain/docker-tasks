# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import sys
from docker_tasks.cli import main

__title__ = 'docker-tasks'
__version__ = '0.1.0'
__author__ = 'Reimund Klain'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Reimund Klain'

if __name__ == '__main__':
    sys.exit(main())