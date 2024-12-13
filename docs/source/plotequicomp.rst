#################
 plotequicomp
#################

*plotequicomp* script shows plasma equilibrium and it is possible to compare equilibrium and its quantities. 
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

************************
 Syntax plotequicomp
************************

   .. command-output:: plotequicomp -h


*************************
 Example plotequicomp
*************************

   .. code-block:: bash

        $ plotequicomp --uri "imas:hdf5?user=public;shot=105027;run=200;database=ITER;version=3" "imas:hdf5?user=public;shot=105027;run=2;database=ITER;version=3"

   .. image:: _static/images/plotequicomp.png
      :alt: image not found
      :align: center
