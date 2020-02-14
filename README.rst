========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-i3-battery-block/badge/?style=flat
    :target: https://readthedocs.org/projects/python-i3-battery-block
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/vgoehler/python-i3-battery-block.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/vgoehler/python-i3-battery-block

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/vgoehler/python-i3-battery-block?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/vgoehler/python-i3-battery-block

.. |requires| image:: https://requires.io/github/vgoehler/python-i3-battery-block/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/vgoehler/python-i3-battery-block/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/vgoehler/python-i3-battery-block/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/vgoehler/python-i3-battery-block

.. |version| image:: https://img.shields.io/pypi/v/i3-battery-block-vgg.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/i3-battery-block-vgg

.. |wheel| image:: https://img.shields.io/pypi/wheel/i3-battery-block-vgg.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/i3-battery-block-vgg

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/i3-battery-block-vgg.svg
    :alt: Supported versions
    :target: https://pypi.org/project/i3-battery-block-vgg

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/i3-battery-block-vgg.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/i3-battery-block-vgg

.. |commits-since| image:: https://img.shields.io/github/commits-since/vgoehler/python-i3-battery-block/v0.3.0.svg
    :alt: Commits since latest release
    :target: https://github.com/vgoehler/python-i3-battery-block/compare/v0.3.0...master



.. end-badges

An i3 wm status block for showing the battery status in i3 blocks. It's output uses pango to format the text. Loosely based on battery2 from James Murphy. https://github.com/vivien/i3blocks-contrib]

* Free software: BSD 2-Clause License

Installation
============

::

    pip install i3-battery-block-vgg

You can also install the in-development version with::

    pip install https://github.com/vgoehler/python-i3-battery-block/archive/master.zip


Command Line Options
====================

.. code:: bash

   usage: i3-battery-block-vgg [-h] [-c] [-b]
                               [-l {debug,info,warning,error,critical}]

   CLI for i3 wm block battery

   optional arguments:
     -h, --help            show this help message and exit
     -c, --compact         flag for compact mode, truncates all batteries into
                           one
     -b, --show_bug        This will show a marker if the acpi bug has occurred.
     -l {debug,info,warning,error,critical}, --loglevel {debug,info,warning,error,critical}
                           log level


Documentation
=============


https://python-i3-battery-block.readthedocs.io/


Development
===========

To run all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
