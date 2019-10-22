.. _installation:

============
Installation
============


Prerequisites
=============

The next requirements will be installed together with Django Tracking Analyzer:

- Django 2.1 or later.
- Django Countries 5.5 or later.
- Django IPWare 2.1.0 or later.
- Django User Agents 0.4.0 or later.
- GeoIP2 2.9.0 or later.


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

- ``'django_user_agents'`` (enables all the functionality needed to get user
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


``install_geoip_dataset`` management command
--------------------------------------------

The management command ``install_geoip_dataset`` is available to help you
download and install the MaxMind GeoLite2 datasets without any effort.

The only thing you have to make is to ensure the existence of the Django setting
``GEOIP_PATH``. This setting specifies the directory where the GeoIP data files
are located. It is unset by default, you have to set it to a directory where you
want the datasets to be installed. A nice place is usually the root directory of
your project code.

Once you have this setting, you can execute the management command and, if you
don't have any GeoLite2 files in that directory, it will download and decompress
the GeoLite2 "City" and "Country" datasets for you::

    python manage.py install_geoip_dataset

In case you already have the datasets installed, the command will ask you if you
really want to download another datasets and replace the existing ones with the
latest downloaded version::

    Seems that MaxMind dataset GeoLite2-Country.mmdb.gz is already installed in "GeoLite2-Country.mmdb.gz". Do you want to reinstall it?
    (y/n)

The process will run for both the "Country" and the "City" datasets.

Although the management command will everything you need in a simlpe run, you
might want to specify some different download options, such the datasets files
names or the download URL. You can do this via the next command parameters:

- ``url``: Base URL where the MaxMind(R) datasets are available.
- ``countries``: Remote file name for the MaxMind(R) Country dataset (compressed).
- ``cities``: Remote file name for the MaxMind(R) City dataset (compressed).


.. _GeoLite2 site: http://dev.maxmind.com/geoip/geoip2/geolite2/
