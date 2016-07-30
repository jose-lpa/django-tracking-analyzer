.. Django Tracking Analyzer documentation master file, created by
   sphinx-quickstart on Sat Jul  9 23:22:40 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================
Django Tracking Analyzer's documentation
========================================

.. rubric:: User actions tracking and analytics for Django sites

.. image:: https://travis-ci.org/jose-lpa/django-tracking-analyzer.svg?branch=master
    :target: https://travis-ci.org/jose-lpa/django-tracking-analyzer

.. image:: https://codecov.io/gh/jose-lpa/django-tracking-analyzer/branch/development/graph/badge.svg
    :target: https://codecov.io/gh/jose-lpa/django-tracking-analyzer

.. image:: https://badge.fury.io/py/django-tracking-analyzer.svg
    :target: https://badge.fury.io/py/django-tracking-analyzer


Overview
========

Django Tracking Analyzer is a Django application that aims to help you know in
a simple and user-friendly way who the visitors of your site are, where they
come from, what devices are they using to browse your site, what resources of
your site they access, when and how many times.

In order to do this, DTA implements a database model ``Tracker``, which will be
created each time a user access certain resource, like a blog post, or performs
certain action, like buying a product in your web shop.

Then, using the Django admin interface, you can check the "Trackers" changelist
in the "Django Tracking Analyzer" app admin, and you will see a changelist of
all the user accesses with details about the requests, like the IP address, the
country and city (if available), the device type, browser and system information.

And also, heading the traditional changelist page, you will be provided with some
nice interactive graphics made in D3.js, to actually see all the data gathered
in a visual fancy way.

===========================
INSERT DASHBOARD IMAGE HERE
===========================


Contents:

.. toctree::
   :maxdepth: 2

   installation
   usage (INCLUDE SOME SCREENSHOTS OF THE DJANGO ADMIN).
   settings
   contributing


License
=======

Licensed under the `GNU GPLv3`_ license.


Source code and contributions
=============================

The source code can be found on Github_.

Bugs can be reported on the Github repository issues. Any collaboration will be
very appreciated. Please see :ref:`contributing` for more details.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Github: https://github.com/jose-lpa/django-tracking-analyzer
.. _GNU GPLv3: http://www.gnu.org/licenses/
