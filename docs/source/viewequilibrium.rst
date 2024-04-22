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

        $ viewequilibrium -p 134174 -r 117 --rho --pfcoils
        $ viewequilibrium --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" --rho --pfcoils

   .. image:: _static/images/EquilibriumView_viewMagneticPoloidalFlux.png
      :alt: image not found
      :align: center

   .. image:: _static/images/PFActiveView_viewActivePfCoils.png
      :alt: image not found
      :align: center
