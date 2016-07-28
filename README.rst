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
.. _GeoIP2 Django documentation: https://docs.djangoproject.com/en/1.10/ref/contrib/gis/geoip2/
.. _PEP-8: https://www.python.org/dev/peps/pep-0008/
.. _Datamaps: https://github.com/markmarkoh/datamaps
.. _TopoJSON: https://github.com/mbostock/topojson
.. _D3 bar chart w/tooltips: http://bl.ocks.org/Caged/6476579
.. _D3 area chart: http://bl.ocks.org/mbostock/3883195
.. _D3.js library: https://d3js.org/
.. _MaxMind: https://www.maxmind.com/