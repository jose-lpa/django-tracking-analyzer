.. _installation:

============
Installation
============

Prerequisites
=============

The next requirements will be installed together with Django Tracking Analyzer:

- Django +1.9 or later.
- Django Countries 3.4.1 or later.
- Django IPWare 1.1.5 or later.
- Django User Agents 0.3.0 or later.
- GeoIP2 2.3.0 or later.

Package installation
====================

You can install the Django Tracking Analyzer package in the two traditional
Python ways:

1. Automatically, by using PyPI (this is of course the preferred way):

.. code-block:: bash

   pip install django-tracking-analyzer

2. Manually, by downloading the package and installing yourself:

.. code-block:: bash

   wget https://github.com/jose-lpa/django-tracking-analyzer/archive/master.zip
   unzip master.zip
   cd django-tracking-analyzer-master/
   python setup.py install

Configuration
=============

Once the package is installed, the next two entries have to be added to the
``INSTALLED_APPS`` setting:

- ``'django_user_agents'`` (enables all the functionalities needed to get user
  agent data)
- ``'tracking_analyzer'``

MaxMind® GeoLite2 datasets installation
=======================================

In order to have IP geolocation and related data collection, DTA uses the
GeoIP2 library, which should have been installed together with this package.

GeoIP2 uses MaxMind® geographical datasets to work, which location is pointed
by the ``GEOIP_PATH`` Django setting. This means you have to dowload and 
install those datasets in the directory specified by that setting, which you 
can do in two different ways:

1. Automatically, by using the DTA management command ``install_geoip_dataset``.
   This is the preferred and fastest way of doing it, and you should be ready
   to go by just running the command: ``python setup.py install_geoip_dataset``.

2. Manually, by downloading yourself the datasets from the MaxMind® `GeoLite2 site`_.

Once this last step is done, you should be ready to use Django Tracking Analyzer.


.. _GeoLite2 site: http://dev.maxmind.com/geoip/geoip2/geolite2/
