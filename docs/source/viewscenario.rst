##############
 viewscenario
##############

*viewscenario* Display the plasma kinetic profiles and equilibrium from
the core_profiles and equilibrium IDSs.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*********************
 Syntax viewscenario
*********************

   .. command-output:: viewscenario -h

Example 
~~~~~~~

   .. code-block:: bash

        $ viewscenario -p 134174 -r 117
        $ viewscenario --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" 
        Time  = 71.44 s in range [10.60,75.00] s
        Index = 53
        Averaged resolution = 0.6133411929278538 s
        summary.global_quantities.energy_mhd.value could not be read
        HMode is not present
        HMode is not present
        HMode is not present
        HMode is not present

   .. thumbnail:: _static/images/viewscenario.png
      :alt: image not found
      :align: center
