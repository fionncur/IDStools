##############
 Installation
##############

*IDStools* is a Python package, so the Python environment is
mandatory. Its functioning depends on IMAS and the data dictionary. As a
result, before running *IDStools* scripts, the IMAS environment must be
loaded.

***********
 For users
***********

Install using pip 

.. code-block:: bash

   $ module load IMAS
   $ git clone ssh://git@git.iter.org/imas/idstools.git
   $ cd idstools
   $ pip install --upgrade pip
   $ pip install --upgrade wheel setuptools
   $ pip install .

Also it is possible to install it in Python virtual environemnt

.. code-block:: bash

   $ module load IMAS
   $ git clone ssh://git@git.iter.org/imas/idstools.git
   $ cd idstools
   $ python -m venv idsenv
   $ source idsenv/bin/activate
   $ pip install .
   $ deactivate

.. note::

   If you are using ITER sdcc cluster then IDStools is available by
   doing module load as shown below

.. code-block:: bash

   $ module load IMAS
   $ module load IDStools/1.14.0-intel-2020b

.. note::

   There are development versions of IDStools on SDCC. These can be used if 
   you need functionlities/bug fixes before next release

.. code-block:: bash

   $ module av -i -t idstools/dev
   /work/imas/etc/modules/all:
   IDStools/dev-gfbf-2022b  
   IDStools/dev-intel-2020b


****************
 For Developers
****************

.. note ::
   Get access to https://git.iter.org/projects/IMAS/repos/idstools 
   repository if you don't have already

Clone *IDStools* repository.

.. code-block:: bash

   $ git clone ssh://git@git.iter.org/imas/idstools.git

If you wish to include additional tools or expanded functionalities,
submit pull requests.

The *IDStools* test suite should be run as follows.:

.. code-block:: bash

   $ cd idstools
   $ pytest

To run example scripts and verify functionalities

.. code-block:: bash

   $ cd idstools
   $ source tests/testscripts.sh

To build the *IDStools* documentation, execute:

.. code-block:: bash

   $ make -C docs html
