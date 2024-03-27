############
 dbselector
############

*dbselector* script shows lists of all scenarios where specified ids is
exists. Just provide idsname as input arguement to the script.

*******************
 Syntax dbselector
*******************

.. code-block:: bash

   $ dbselector -h
   Install tqdm to enable progress bar
   usage: dbselector [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] ids

   Checks if spciefied ids is exists in scenario database

   positional arguments:
   ids                   Name of the IDS to check if it is available in scenario

   optional arguments:
   -h, --help            show this help message and exit
   -u USER, --user_or_path USER
                           user (default=public)
   --database DATABASE, -d DATABASE
                           database name (default=ITER)
   --backend BACKEND, -b BACKEND
                           backend format (default=MDSPLUS)
   --version VERSION, -v VERSION
                           data version (default=3)

********************
 Example dbselector
********************

.. code-block:: bash

   $ dbselector edge_profiles
   (123148, 4)
   (123285, 1)
   (123166, 2)
   (112325, 3)
   (102425, 2)
   (123305, 1)
   (103034, 3)
