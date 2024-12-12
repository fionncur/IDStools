##############
 plotpressure
##############

*plotpressure* Display the plasma kinetic profiles from the
core_profiles IDSs, It shows ion and electrons pressure properties from
core_profiles.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*********************
 Syntax plotpressure
*********************

   .. command-output:: plotpressure -h

*********
 Example
*********

   .. code-block:: bash

        $ plotpressure --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3"
        Time  = 71.44 s in range [10.60,75.00] s
        Index = 53
        Averaged resolution = 0.6133411929278538 s
        Empty profiles_1d[0].pressure_fast_parallel
        Empty profiles_1d[0].pressure_fast_perpendicular
        Empty profiles_1d[0].electrons.pressure
        Empty profiles_1d[0].electrons.pressure_fast_parallel
        Empty profiles_1d[0].electrons.pressure_fast_perpendicular
        Total volume:83036.75126289157
        Empty profiles_1d[0].ion.pressure_fast_parallel
        Empty profiles_1d[0].ion.pressure_fast_perpendicular
        Empty profiles_1d[0].electrons.pressure
        Empty profiles_1d[0].electrons.pressure_fast_parallel
        Empty profiles_1d[0].electrons.pressure_fast_perpendicular

   .. image:: _static/images/plotpressure.png
      :alt: image not found
      :align: center
