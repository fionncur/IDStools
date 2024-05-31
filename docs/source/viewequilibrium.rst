#################
 viewequilibrium
#################

*viewequilibrium* script shows plasma equilibrium. Optionally it also
shows pf coils position and toroidal flux.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

************************
 Syntax viewequilibrium
************************

   .. command-output:: viewequilibrium -h


*************************
 Example viewequilibrium
*************************

   .. code-block:: bash

        $ viewequilibrium --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" --rho -mdesc pf_active wall
        $ viewequilibrium --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" --rho -mdesc "imas:mdsplus?user=public;pulse=111001;run=103;database=ITER_MD;version=3#pf_active" "imas:mdsplus?user=public;pulse=116000;run=4;database=ITER_MD;version=3#wall"
        $ viewequilibrium --uri "imas:mdsplus?user=public;pulse=134173;run=2326;database=TEST;version=3" --rho --mdesc "imas:mdsplus?user=public;pulse=111001;run=103;database=ITER_MD;version=3#pf_active" "imas:hdf5?user=public;pulse=116000;run=4;database=ITER_MD;version=3#wall"
        
   .. thumbnail:: _static/images/viewequilibrium.png
      :alt: image not found
      :align: center

   .. thumbnail:: _static/images/viewequilibrium2.png
      :alt: image not found
      :align: center
