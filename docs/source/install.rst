##############
 Installation
##############

Because *IDSTools* is a Python package, the Python environment is
required. Its functioning depends on IMAS and the data dictionary. As a
result, before running *IDSTools* scripts, the IMAS environment must be
loaded.

***********
 For users
***********

Install using pip

.. code-block:: bash

   git clone ssh://git@git.iter.org/imas/idstools.git
   cd idstools
   pip install --upgrade pip
   pip install --upgrade wheel setuptools
   pip install .

.. note::

   If you are using ITER sdcc cluster then IDSTools is available by
   doing module load as shown below

.. code-block:: bash

   module load IMAS
   module load IDStools/1.14.0-intel-2020b

In addition, several versions of *IDSTools* are available on the
cluster.

.. code-block:: bash

   module av -i idstools
   # IDStools/1.14.0-gfbf-2022b
   # IDStools/1.14.0-intel-2020b

****************
 For Developers
****************

Clone *IDSTools* repository.

.. code-block:: bash

   git clone ssh://git@git.iter.org/imas/idstools.git

If you wish to include additional tools or expanded functionalities,
submit pull requests.

The *IDSTools* test suite should be run as follows.:

.. code-block:: bash

   cd idstools
   pytest

To build the *IDSTools* documentation, execute:

.. code-block:: bash

   make -C docs html
