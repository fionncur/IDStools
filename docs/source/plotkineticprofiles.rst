#####################
 plotkineticprofiles
#####################

*plotkineticprofiles* shows plasma kinetic profiles from the
core_profiles IDSs
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

****************************
 Syntax plotkineticprofiles
****************************

   .. command-output:: plotkineticprofiles -h

*****************************
 Example plotkineticprofiles
*****************************

   .. code-block:: bash

        $ plotkineticprofiles --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3"
        Time  = 71.44 s in range [10.60,75.00] s
        Index = 53
        Averaged resolution = 0.6133411929278538 s
        Time  = 71.44 s in range [1.20,149.44] s
        Index = 53
        Averaged resolution = 1.4117675982100488 s
        Ti_flag : 1, Ti_e_flag : 0
        ------------
        species:      D       T       Be
        a:            2.0     3.0     9.0
        z:            1.0     1.0     4.0
        n_over_ntot:  0.504   0.495   0.001
        n_over_ne:    0.502   0.494   0.001
        n_over_n_maj: 1.000   0.984   0.002

   .. image:: _static/images/plotkineticprofiles.png
      :alt: image not found
      :align: center
