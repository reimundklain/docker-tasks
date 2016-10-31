|travis|

docker-tasks
############

``docker-tasks`` is a tool for executing periodic tasks via docker exec.
It is looking up for running docker images and execute the specified commands in the matching container

An use case could be to dump all `PostgreSQL <https://www.postgresql.org/>`__ based images to the container related volume.
This allow me to backup ``/var/lib/docker/volumes/`` with a ``pg_dump`` generated database dump inside my volumes.

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
      -v, --verbose         Increase output verbosity


.. |travis| image:: https://travis-ci.org/daymien/docker-tasks.svg
   :target: https://travis-ci.org/daymien/docker-tasks