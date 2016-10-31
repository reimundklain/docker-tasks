docker-tasks
############

``docker-tasks`` is a tool for executing periodic tasks via docker exec.
For example dumping all `PostgreSQL <https://www.postgresql.org/>`__ based images to the container related volume.

Installation
============

::

    pip install docker-tasks


Create a ``docker-tasks.yml`` with example commands

::

    images:
        ubuntu:
          '*':
            - ps aux

        postgres:
          '9.*':
            - /bin/sh -c "pg_dump -U postgres postgres > /var/lib/postgresql/data/db_backup_$(date +%u).sql"

Usage
=====

::

    usage: docker-tasks [-h] [-c CONFIG] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Config yaml. Default (docker-tasks.yml)
      -v, --verbose         Increate output verbosity