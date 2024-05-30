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

        $ viewequilibrium -p 134174 -r 117 --rho 
        $ viewequilibrium --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" --rho pf_active wall
        $ viewequilibrium -p 134174 -r 117 --rho -mdesc "imas:mdsplus?user=public;shot=111001;run=103;database=ITER_MD;version=3#pf_active" "imas:mdsplus?user=public;shot=116000;run=4;database=ITER_MD;version=3#wall"
        $ viewequilibrium -uri "imas:hdf5?user=sawantp1;shot=100028;run=1;database=MYDB;version=3" -mdesc "imas:mdsplus?user=costerd;shot=40866;run=1;database=aug;version=3#wall" --show-labels
        
   .. thumbnail:: _static/images/viewequilibrium.png
      :alt: image not found
      :align: center

   .. thumbnail:: _static/images/viewequilibrium2.png
      :alt: image not found
      :align: center
