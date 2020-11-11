.. standard_names documentation master file, created by
   sphinx-quickstart on Fri Jul 22 11:31:51 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

standard_names: a Python library for working with CSDMS Standard Names
======================================================================

The CSDMS Standard Names provide a comprehensive set of naming rules
and patterns that are not specific to any particular modeling domain.
They were also designed to have many other nice features such as parsability
and natural alphabetical grouping. CSDMS Standard Names always consist of
an object part and a quantity/attribute part and the quantity part may
also have an operation prefix which can consist of multiple operations
([CsdmsCsn]_, [Peckham2014]_).

*standard_names* is a Python package to define, query, operatate, and
manipulate CSDMS Standard Names. It is distributed with a comprehensive
list of the currently defined Standard Names [StandardNamesRegistry]_.

The *standard_names* package consists of two basic classes:

*  :py:class:`~.StandardName`: a single name
*  :py:class:`~.NamesRegistry`: a collection of names.

The standard_names package has a complete set up unit tests that are
continually tested on Mac, Linux, and Windows. It is distributed both
as source code [StandardNamesGitHub]_ and as Anaconda packages from
Anaconda Cloud.

Standard Names is an element of the `CSDMS Workbench`_,
an integrated system of software tools, technologies, and standards
for building and coupling models.

.. _CSDMS Workbench: https://csdms.colorado.edu/wiki/Workbench


Quickstart
----------

Install the ``standard_names`` package:

.. code:: bash

  $ conda install standard_names -c csdms

Import the ``standard_names`` package:

.. code:: python

  >>> import standard_names as csn


Create a standard name from a string.

.. code:: python

  >>> name = csn.StandardName('air__temperature')
  >>> name.object, name.quantity
  ('air', 'temperature')

Get a registry of the currently defined standard names.

.. code:: python

  >>> registry = csn.NamesRegistry()
  >>> len(registry)
  2652
  >>> 'air__temperature' in registry
  True

User Guide
----------

.. toctree::
  :maxdepth: 1

  getting

References
==========

.. [Peckham2014] `Extended abstract <http://csdms.colorado.edu/mediawiki/images/Peckham_2014_iEMSs.pdf>`_ from IEMSS 2014.

  Peckham, S. D, 2014. *The CSDMS Standard Names: Cross-Domain Naming
  Conventions for Describing Process Models, Data Sets and Their Associated
  Variables*, 7th International Conference on Environmental Modeling and
  Software,, International Environmental Modelling and Software Society.

.. [CsdmsCsn] Detailed description of CSDMS Standard Names

  http://csdms.colorado.edu/wiki/CSDMS_Standard_Names

.. [StandardNamesGitHub] The standard_names source code on GitHub.

  https://github.com/csdms/standard_names

.. [StandardNamesRegistry] The current Standard Names Registry on GitHub.

  https://github.com/csdms/standard_names_registry

.. [CfStandardNames] CF Standard Names for ocean and atmosphere modeling.

  http://cfconventions.org/Data/cf-standard-names/27/build/cf-standard-name-table.html

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

