############
 dbselector
############

*dbselector* script shows lists of all db entries where specified ids is
exists. Just provide idsname as input argument to the script.

*******************
 Syntax dbselector
*******************

   .. command-output:: dbselector -h

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

.. code-block:: bash

   $ dbselector -u $USER equilibrium,core_sources
   (100016, 1)
   (134000, 37)
   (134173, 106)
   (110014, 1)
   (100300, 1)
   (101051, 1)

