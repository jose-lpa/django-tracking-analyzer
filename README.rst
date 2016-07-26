========================
Django Tracking Analyzer
========================

User actions tracking and analytics for Django sites

.. image:: https://travis-ci.org/jose-lpa/django-tracking-analyzer.svg?branch=master
    :target: https://travis-ci.org/jose-lpa/django-tracking-analyzer

.. image:: https://codecov.io/gh/jose-lpa/django-tracking-analyzer/branch/development/graph/badge.svg
    :target: https://codecov.io/gh/jose-lpa/django-tracking-analyzer

.. image:: https://badge.fury.io/py/django-tracking-analyzer.svg
    :target: https://badge.fury.io/py/django-tracking-analyzer


Requirements
============

- Django 1.9 or later.
- `Django Countries`_ 3.4.1 or later.
- `Django IPWare`_ 1.1.5 or later.
- `Django User Agents`_ 0.3.0 or later.
- `GeoIP2 2.3.0`_ or later.
- `MaxMind GeoLite2 country datasets`_.


Installation
============

Install Django Tracking Analyzer from PyPI by using ``pip``::

    pip install django-tracking-analyzer


Contribution
============

All contributions or fixes are welcome. Just make sure to follow this rules:

- Always include some unit tests for the new code you write or the bugs you fix. Or, update the existent unit tests, if necessary.
- Stick to PEP-8_ styling.
- Make your pull requests to ``development`` branch.

Testing
-------

Run tests::

    python setup.py test

Run tests with coverage::

    python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes"

Run tests with coverage and Pylint/PEP8 checking::

    python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes --pylint --pylint-rcfile=pylint.rc --pep8"


Acknowledgements
================

Django Tracking Analyzer makes use of this technologies and apps, without which it wouldn't be possible:

- `Django Countries`_, by Chris Beaven.
- `Django IPWare`_, by Val Neekman.
- `Django User Agents`_, by Selwin Ong.
- Datamaps_, by Marc DiMarco.
- TopoJSON_, by Mike Bostock.
- `D3 bar chart w/tooltips`_, original code by Justin Palmer.
- `D3 area chart`_, by Mike Bostock.
- Of course, the `D3.js library`_.
- And MaxMind_, the company behind all the geographical datasets that made them publicly available.


.. _Django Countries: https://pypi.python.org/pypi/django-countries
.. _Django IPWare: https://pypi.python.org/pypi/django-ipware
.. _Django User Agents: https://pypi.python.org/pypi/django-user_agents
.. _GeoIP2 2.3.0: https://pypi.python.org/pypi/geoip2
.. _MaxMind GeoLite2 country datasets: http://dev.maxmind.com/geoip/geoip2/geolite2/
.. _PEP-8: https://www.python.org/dev/peps/pep-0008/
.. _Datamaps: https://github.com/markmarkoh/datamaps
.. _TopoJSON: https://github.com/mbostock/topojson
.. _D3 bar chart w/tooltips: http://bl.ocks.org/Caged/6476579
.. _D3 area chart: http://bl.ocks.org/mbostock/3883195
.. _D3.js library: https://d3js.org/
.. _MaxMind: https://www.maxmind.com/