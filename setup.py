#!/usr/bin/env python
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='django-tracking-analyzer',
    version='0.1a1',
    description='User actions tracking and analytics for Django sites.',
    author='Jose Luis Patino Andres',
    author_email='jose.lpa@gmail.com',
    url='https://github.com/jose-lpa/django-tracking-analyzer',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Django>=1.7',
        'django-countries',
        'django-ipware',
        'django-user-agents',
        'geoip2'
    ],
    test_suite='tests',
    tests_require=[
        'factory-boy',
        'pytest-django',
        'pytest-cov',
        'pytest-pep8',
        'pytest-pylint',
    ],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ]
)
