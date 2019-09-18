
Python library *putcall*
------------------------

.. image:: https://img.shields.io/codeship/621a4060-ba8a-0137-eb4a-4a1d2f2d4303/master.svg
   :target: https://codeship.com//projects/364830
   :alt: CodeShip

.. image:: https://travis-ci.org/sonntagsgesicht/putcall.svg?branch=master
   :target: https://travis-ci.org/sonntagsgesicht/putcall
   :alt: Travis ci

.. image:: https://img.shields.io/readthedocs/putcall
   :target: http://putcall.readthedocs.io
   :alt: Read the Docs

.. image:: https://img.shields.io/codefactor/grade/github/sonntagsgesicht/putcall/master
   :target: https://www.codefactor.io/repository/github/sonntagsgesicht/putcall
   :alt: CodeFactor Grade

.. image:: https://img.shields.io/codeclimate/maintainability/sonntagsgesicht/putcall
   :target: https://codeclimate.com/github/sonntagsgesicht/putcall/maintainability
   :alt: Code Climate maintainability

.. image:: https://img.shields.io/codecov/c/github/sonntagsgesicht/putcall
   :target: https://codecov.io/gh/sonntagsgesicht/putcall
   :alt: Codecov

.. image:: https://img.shields.io/lgtm/grade/python/g/sonntagsgesicht/putcall.svg
   :target: https://lgtm.com/projects/g/sonntagsgesicht/putcall/context:python/
   :alt: lgtm grade

.. image:: https://img.shields.io/lgtm/alerts/g/sonntagsgesicht/putcall.svg
   :target: https://lgtm.com/projects/g/sonntagsgesicht/putcall/alerts/
   :alt: total lgtm alerts

.. image:: https://img.shields.io/github/license/sonntagsgesicht/putcall
   :target: https://github.com/sonntagsgesicht/putcall/raw/master/LICENSE
   :alt: GitHub

.. image:: https://img.shields.io/github/release/sonntagsgesicht/putcall?label=github
   :target: https://github.com/sonntagsgesicht/putcall/releases
   :alt: GitHub release

.. image:: https://img.shields.io/pypi/v/putcall
   :target: https://pypi.org/project/putcall/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/putcall
   :target: https://pypi.org/project/putcall/
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/dm/putcall
   :target: https://pypi.org/project/putcall/
   :alt: PyPI Downloads

Collection of classical option pricing formulas.


Example Usage
-------------

.. code-block::

    >>> from putcall import black_scholes

    >>> spot_value = 100
    >>> strike_value = 105
    >>> vol_value = 0.2
    >>> time_value = 2.0
    >>> is_call_bool = True
    >>> rate = 0.05

    >>> black_scholes(spot_value, strike_value, vol_value, time_value, is_call_bool, rate)
    13.639602713024757


Install
-------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install putcall

If the above fails, please try easy_install instead:

.. code-block:: bash

    $ easy_install putcall


Development Version
-------------------

The latest development version can be installed directly from GitHub:

.. code-block:: bash

    $ pip install --upgrade git+https://github.com/pbrisk/putcall.git


Contributions
-------------

.. _issues: https://github.com/pbrisk/putcall/issues
.. __: https://github.com/pbrisk/putcall/pulls

Issues_ and `Pull Requests`__ are always welcome.


License
-------

.. __: https://github.com/pbrisk/putcall/raw/master/LICENSE

Code and documentation are available according to the Apache Software License (see LICENSE__).


