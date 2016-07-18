# Django Tracking Analyzer
User actions tracking and analytics for Django sites

[![Build Status](https://travis-ci.org/jose-lpa/django-tracking-analyzer.svg?branch=master)](https://travis-ci.org/maykinmedia/django-tracking-analyzer)
[![PyPI version](https://badge.fury.io/py/django-tracking-analyzer.svg)](https://badge.fury.io/py/django-tracking-analyzer)

## Contribution

### Testing
Run tests:
    python setup.py test
Run tests with coverage:
    python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes"
Run tests with coverage and Pylint/PEP8 checking:
    python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes --pylint --pylint-rcfile=pylint.rc --pep8"
