docker-tasks
############

docker-tasks is a tool for executing periodic tasks via docker exec.
For example dumping all postgres based images to there local volume.

docker-tasks.yml
================

.. code-block::

  images:
      postgres:
        '9.*':
          - /bin/sh -c "pg_dump -U postgres postgres > /var/lib/postgresql/data/db_backup_$(date +%u).sql"