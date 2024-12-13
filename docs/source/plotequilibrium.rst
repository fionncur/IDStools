#################
 plotequilibrium
#################

*plotequilibrium* script shows plasma equilibrium. Optionally it also
shows pf coils position and toroidal flux.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

************************
 Syntax plotequilibrium
************************

   .. command-output:: plotequilibrium -h


*************************
 Example plotequilibrium
*************************

   .. code-block:: bash

        $ plotequilibrium --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" --rho -md pf_active wall --plots
        $ plotequilibrium --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" --rho -md "imas:mdsplus?user=public;pulse=111001;run=103;database=ITER_MD;version=3#pf_active" "imas:mdsplus?user=public;pulse=116000;run=4;database=ITER_MD;version=3#wall"
        $ plotequilibrium --uri "imas:mdsplus?user=public;pulse=134173;run=2326;database=TEST;version=3" --rho --md "imas:mdsplus?user=public;pulse=111001;run=103;database=ITER_MD;version=3#pf_active" "imas:hdf5?user=public;pulse=116000;run=4;database=ITER_MD;version=3#wall"
        
   .. image:: _static/images/plotequilibrium.png
      :alt: image not found
      :align: center

   .. image:: _static/images/plotequilibrium2.png
      :alt: image not found
      :align: center

   .. image:: _static/images/plotequilibrium3.png
      :alt: image not found
      :align: center