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
        $ viewequilibrium -p 134174 -r 117 --rho pf_active/111001/103/public/MDSPLUS/ITER_MD/3 wall/"imas:mdsplus?user=public;shot=116000;run=4;database=ITER_MD;version=3"

   .. thumbnail:: _static/images/viewequilibrium.png
      :alt: image not found
      :align: center

