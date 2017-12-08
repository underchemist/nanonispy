|Build Status| |Coverage Status| |Install with conda|

nanonispy
=========

A small library written in python 3 to parse Nanonis binary and ascii
files.

Nanonispy was made in needing to do a lot of analysis for scanning tunneling microscopy (STM) data, and thought this would be good practice in creating a proper python library. That being said it is in no way foolproof and if anybody else actually uses this please let me know if you run into issues.

Nanonispy can read Nanonis grid, scan, and point spectroscopy files. This means it will read the file header and parse that into a somewhat useful dictionary for later use, as well as read in the binary/ascii data in a relatively general way to accomadate data with multiple channels stored, or custom spectroscopy experiments.

Requirements
------------

Currently written and tested with

- python 3.6
- python 3.5
- python 3.4

**dropping support for python 3.3 due to matplotlib no longer supporting it**

Depends on

- numpy


Install
-------
For the most up-to-date version, install from github as pip and conda packages are not updated as frequently.

pip
~~~

::

    pip install nanonispy

conda
~~~~~

::

    conda install --channel https://conda.anaconda.org/underchemist nanonispy

github
~~~~~~

Simply clone this repo and run

::

    python setup.py install

Basic usage
-----------

Once installed, you should be able to import it to any python script or ipython session.

.. code:: python

    import nanonispy as nap

Then given a file,

.. code:: python

    grid = nap.read.Grid('/path/to/datafile.3ds')

You can look at the attributes and methods to determine the information
available.

Running tests
-------------

Similar to the install, except run

::

    python setup.py test

. If you have the nose module installed, it's as simple as

::

    nosetests

.

You can also see coverage of the tests as well as ignore the test
discovery of numpy core packages (don't quite understand why it does
this) with

::

    nosetests --with-coverage --cover-branches --cover-package=nanonispy

.


.. |Build Status| image:: https://travis-ci.org/underchemist/nanonispy.svg?branch=master
   :target: https://travis-ci.org/underchemist/nanonispy
.. |Coverage Status| image:: https://coveralls.io/repos/underchemist/nanonispy/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/underchemist/nanonispy?branch=master
.. |Install with conda| image:: https://anaconda.org/underchemist/nanonispy/badges/installer/conda.svg
   :target: https://anaconda.org/underchemist/nanonispy/badges/installer/conda.svg
