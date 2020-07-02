#!/usr/bin/env python

import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


with open('README.rst', 'r') as readme:
    long_description = readme.read()


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
    version='1.1.1',
    description='User actions tracking and analytics for Django sites.',
    long_description=long_description,
    author='José Luis Patiño Andrés',
    author_email='jose.lpa@gmail.com',
    url='https://github.com/jose-lpa/django-tracking-analyzer',
    keywords=['django', 'analytics', 'web', 'monitoring', 'logging'],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'Django>=2.1',
        'django-appconf',
        'django-countries',
        'django-ipware>=3.0',
        'django-user-agents',
        'geoip2'
    ],
    test_suite='tests',
    tests_require=[
        'factory-boy',
        'pytest-django',
        'pytest-cov',
        'pytest-pycodestyle',
        'pytest-pylint',
    ],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ]
)
