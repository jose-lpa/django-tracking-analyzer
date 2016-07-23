========================
Django Tracking Analyzer
========================

User actions tracking and analytics for Django sites

.. image:: https://travis-ci.org/jose-lpa/django-tracking-analyzer.svg?branch=master
    :target: https://travis-ci.org/maykinmedia/django-tracking-analyzer

.. image:: https://codecov.io/gh/jose-lpa/django-tracking-analyzer/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jose-lpa/django-tracking-analyzer

.. image:: https://badge.fury.io/py/django-tracking-analyzer.svg
    :target: https://badge.fury.io/py/django-tracking-analyzer

Contribution
============

All contributions or fixes are welcome. Just make sure to follow this rules:

- Always include some unit tests for the new code you write or the bugs you fix. Or, update the existent unit tests, if necessary.
- Stick to PEP-8_ styling.
- Make your pull requests to `develop` branch.

Testing
-------

Run tests::

    python setup.py test

Run tests with coverage::

    python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes"

Run tests with coverage and Pylint/PEP8 checking::

    python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes --pylint --pylint-rcfile=pylint.rc --pep8"

.. _PEP-8: https://www.python.org/dev/peps/pep-0008/