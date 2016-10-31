docker-tasks
############

``docker-tasks`` is a tool for executing periodic tasks via docker exec.
For example dumping all `PostgreSQL <https://www.postgresql.org/>`__ based images to the container related volume.

Installation
============

::

    pip install docker-tasks


docker-tasks.yml
________________

::

    images:
        postgres:
          '9.*':
            - /bin/sh -c "pg_dump -U postgres postgres > /var/lib/postgresql/data/db_backup_$(date +%u).sql"