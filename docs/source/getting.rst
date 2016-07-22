Installation
============

*standard_names* has no dependencies other than Python itself. It
runs on Python 2.7 and 3.x.

You can install it with conda from the csdms channel on Anaconda Cloud,

.. code:: bash

  $ conda install standard_names -c csdms

After installing, you can check to see that everything installed
correctly by starting Python and trying to import ``standard_names``.

.. code:: python

  >>> import standard_names as csn
  >>> csn.__version__
  0.2.2
  >>> csn.check()


Getting the code
----------------

You can also get the source code from GitHub. You can either clone it
with ``git``:

.. code:: bash

  $ git clone git@github.com:csdms/standard_names

or download a snapshot of the latest code with either

.. code:: bash

  $ curl -OL https://github.com/csdms/standard_names/tarball/master

(for a ``.tar.gz`` file) or

.. code:: bash

  $ curl -OL https://github.com/csdms/standard_names/zipball/master

(for a ``.zip`` file).

Now that you have the source code, install it in your Python distribution
with:

.. code:: bash

  $ python setup.py install
