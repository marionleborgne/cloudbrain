Status
======

|Build Status|

Features
========

CloudBrain is a platform for real-time sensor data analysis and
visualization. 

- **Stream sensor data** in a unified format. 
- **Store sensor data** in a central database. 
- **Analyze sensor data** to find patterns. 
- **Visualize sensor data** and patterns in real-time.

.. figure:: https://raw.githubusercontent.com/cloudbrain/cloudbrain/master/docs/images/features.png
   :alt: features

Using CloudBrain
================

Setup
-----

-  Run: ``pip install . --user``
-  If you plan to *edit* the code, make sure to use the ``-e`` switch:
   ``pip  install -e . --user``

Optional
--------

Optional CloudBrain modules can be installed: 

- Muse source module: ``pip install .[muse] --user`` *(Python ``3.*`` only)* 

Run the tests
-------------

::

    python setup.py test

Docker (experimental)
---------------------

Docker can be used to start modules that don't require connecting to the
host machine. It's useful for running the mock source (signal generator)
and other processing modules.

::

    docker build -t cloudbrain .
    docker run -it -v /path/to/config:/config cloudbrain \
        --file /config/name.of.config.file.json

When running other services on a docker network:

::

    docker network create cloudbrain_network
    docker run -it -v /path/to/config:/config cloudbrain \
        --network cloudbrain_network \
        --file /config/name.of.config.file.json

Docker Compose (experimental)
-----------------------------

The docker compose setup expects a cloudbrain\_network to already be set
up with a rabbitmq server named mock-rabbit running. The compose file
will load the configuration at ./examples/source.mock.docker.json which
can be modified as desired. This will not currently run modules that
require connecting to the host machine. It's useful for running the mock
source (signal generator) and other processing modules.

::

    docker network create cloudbrain_network
    docker run -d --hostname mock-rabbit --name mock-rabbit \
        --network cloudbrain_network \
        -p 8080:15672 -p 5672:5672 rabbitmq:3-management
    docker-compose up

Examples
--------

See ``README.md`` in ``cloudbrain/examples`` for more information about
how to use and chain CloudBrain modules.

More docs
---------

For more details on to setup and use CloudBrain, refer to the
`wiki <https://github.com/cloudbrain/cloudbrain/wiki>`__.

License
~~~~~~~

|License: AGPL-3|

.. |Build Status| image:: https://travis-ci.org/cloudbrain/cloudbrain.svg?branch=master
   :target: https://travis-ci.org/cloudbrain/cloudbrain
.. |License: AGPL-3| image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://raw.githubusercontent.com/cloudbrain/cloudbrain/master/LICENSE.md
