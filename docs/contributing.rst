.. _contributing:

============
Contributing
============

If you want to add some functionality or you spot a bug and you want to fix it
yourself, you can fork the Github repository and make all your changes in your
local clone.

Once you are done, please submit all your changes by issuing a pull request.

When you are writing your code, please take into account the following basic
rules:

- Always include some unit tests for the new code you write or the bugs you fix. Or, update the existent unit tests, if necessary.
- Stick to PEP-8_ styling.

Testing
=======

We use Pytest to unit test Django Tracking Analyzer. You can run the tests in
your local in 3 different ways, depending on what you want to check:

Simply run the unit tests. This should be enough for everybody::

   python setup.py test

Run tests with code coverage analysis::

   python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes"

Run tests with coverage and Pylint/PEP8 checking::

   python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes --pylint --pylint-rcfile=pylint.rc --pep8"

Versioning
==========

Compliance API uses bumpversion_
package to manage versioning. You can install bumpversion regularly via `pip`::

    pip install bumpversion

You can now bump parts of version.

Version bumps with examples:

* ``bumpversion patch``: ``0.1.0 -> 0.1.1``
* ``bumpversion minor``: ``0.1.1 -> 0.2.0``
* ``bumpversion major``: ``0.2.0 -> 1.0.0``

**Warning:** Each version bump will also create commit with tag.


.. _PEP-8: https://www.python.org/dev/peps/pep-0008/
.. _bumpversion: https://pypi.python.org/pypi/bumpversion
