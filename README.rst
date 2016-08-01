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

.. image:: https://readthedocs.org/projects/django-tracking-analyzer/badge/?version=latest
    :target: http://django-tracking-analyzer.readthedocs.io/en/latest/?badge=latest


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

1. Install Django Tracking Analyzer from PyPI by using ``pip``::

    pip install django-tracking-analyzer


2. Add ``'django_user_agents'`` and ``'tracking_analyzer'`` entries to Django ``INSTALLED_APPS`` setting.
3. Run the migrations to load the ``Tracker`` model in your database::

    python manage.py migrate tracking_analyzer


4. Install the MaxMind® GeoIP2 datasets. You can do this in two ways:

   4.1. By running the provided management command for this::

        python manage.py install_geoip_dataset


   4.2. Or manually, by following the instructions in `GeoIP2 Django documentation`_.

After following those steps, you should be ready to go.


Explanation - Quickstart
========================

Django Tracking Analyzer is a Django pluggable application which helps you
providing usage statistics and visitors data for your Django sites.

DTA does this by recording requests data in those places you want to by saving
``Tracker``'s. A ``Tracker`` is a Django database model which holds all the
data related to a request, including geolocation via IP address and device or
browser specifications.

When some data is collected, the Django admin interface for ``Tracker`` model
implements some interactive widgets to help you visualize better the data.


Now let's see how can you start collecting users data. Imagine the most basic
example: you have a web blog and you want to check the visits to your posts,
having a resume of who accessed the posts, when and from where. In such a Django
site, you might have a view ``PostDetailView``, where a blog post will be served
by passing its slug in the URL. Something like this:

.. code-block:: python

    class PostDetailView(DetailView):
        model = Post


Okay, so you can track the users who access blog posts by their instances with
DTA, just like this:

.. code-block:: python

    class PostDetailView(DetailView):
        model = Post

        def get_object(self, queryset=None):
            # Retrieve the blog post just using `get_object` functionality.
            obj = super(PostDetailView, self).get_object(queryset)

            # Track the users access to the blog by post!
            Tracker.objects.create_from_request(self.request, obj)

            return obj


And you are now on your way to collect users data! Now give it a time (or better
access the resource yourself several times) and go check your Django admin in
the "Django Tracking Analyzer" - "Trackers" section. Enjoy!


Documentation
=============

For extensive documentation and usage explanations, you can check `Read the Docs`_.


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
.. _GeoIP2 Django documentation: https://docs.djangoproject.com/en/1.10/ref/contrib/gis/geoip2/
.. _Read the Docs: http://django-tracking-analyzer.readthedocs.io/en/latest/
.. _Datamaps: https://github.com/markmarkoh/datamaps
.. _TopoJSON: https://github.com/mbostock/topojson
.. _D3 bar chart w/tooltips: http://bl.ocks.org/Caged/6476579
.. _D3 area chart: http://bl.ocks.org/mbostock/3883195
.. _D3.js library: https://d3js.org/
.. _MaxMind: https://www.maxmind.com/
