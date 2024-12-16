##############
 plotrotation
##############

*plotrotation* Display the plasma kinetic profiles from the
core_profiles IDSs.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*********************
 Syntax plotrotation
*********************

   .. command-output:: plotrotation -h

*********
 Example
*********

   .. code-block:: bash

        $ plotrotation --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3"
        Time  = 75.00 s in range [10.60,75.00] s
        Index = 105
        Averaged resolution = 0.6133411929278538 s
        core_profiles.profiles_1d[0].ion[0].velocity.diamagnetic could not be read
        core_profiles.profiles_1d[0].ion[1].velocity.diamagnetic could not be read
        core_profiles.profiles_1d[0].ion[2].velocity.diamagnetic could not be read

   .. image:: _static/images/plotrotation.png
      :alt: image not found
      :align: center
