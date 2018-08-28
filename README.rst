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

Installing
----------
Cloudbrain is available for download via `PyPI <https://pypi.python.org/pypi/cloudbrain>`_ and may be installed using ``pip``:

::

    pip install cloudbrain


Installing additional modules
-----------------------------

Optional CloudBrain modules can be installed:

- Analytics modules: ``pip install cloudbrain[analytics]``
- `Muse <http://www.choosemuse.com>`_ source module: ``pip3 install cloudbrain[muse]`` (Python ``3.*`` only)


Installing from source
----------------------

-  Clone this repository and run ``pip install .`` from the root of the repo.
-  If you plan to *edit* the code, make sure to use the ``-e`` switch:
   ``pip  install -e .``


Running the tests
-----------------
Analytics modules need to be installed prior to running the tests. See instalation section.
::

    python setup.py test


Examples
--------

See ``README.md`` in ``cloudbrain/examples`` for more information about
how to use CloudBrain analytics modules.

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
