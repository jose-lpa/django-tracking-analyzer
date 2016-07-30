.. _contributing:


============
Contributing
============

If you want to add some functionality or you spot a bug and you want to fix it
yourself, you can fork the Github repository and make all your changes in your
local clone.

Once you are done, please submit all your changes by issuing a pull request
against the ``development`` branch.

When you are writing your code, please take into account the following basic
rules:

- Always include some unit tests for the new code you write or the bugs you fix. Or, update the existent unit tests, if necessary.
- Stick to PEP-8_ styling.
- Make your pull requests to ``development`` branch.

Testing
=======

We use Pytest to unit test Django Tracking Analyzer. You can run the tests in
your local in 3 different ways, depending on what you want to check:

1. Simply run the unit tests. This should be enough for everybody::

   python setup.py test

2. Run tests with code coverage analysis::

   python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes"

3. Run tests with coverage and Pylint/PEP8 checking::

   python setup.py test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --verbose --junit-xml=junit.xml --color=yes --pylint --pylint-rcfile=pylint.rc --pep8"

The last one will probably fail ;) but don't worry too much about that. Just
make sure that at least the 1st testing command works well without any errors.


.. _PEP-8: https://www.python.org/dev/peps/pep-0008/
