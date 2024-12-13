##############
 plotscenario
##############

*plotscenario* Display the plasma kinetic profiles and equilibrium from
the core_profiles and equilibrium IDSs.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*********************
 Syntax plotscenario
*********************

   .. command-output:: plotscenario -h

Example 
~~~~~~~

   .. code-block:: bash

        $ plotscenario --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" 
        Time  = 71.44 s in range [10.60,75.00] s
        Index = 53
        Averaged resolution = 0.6133411929278538 s
        summary.global_quantities.energy_mhd.value could not be read
        HMode is not present
        HMode is not present
        HMode is not present
        HMode is not present

   .. image:: _static/images/plotscenario.png
      :alt: image not found
      :align: center
