#############
 viewneutron
#############

*viewneutron* plots particles vs normalised toroidal flux coordinate. It
retrieves from distribution_sources IDS
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

********************
 Syntax viewneutron
********************

   .. command-output:: viewneutron -h

*********
 Example
*********

   .. code-block:: bash

        $ viewneutron --uri "imas:mdsplus?user=public;pulse=121014;run=11;database=ITER;version=3" -t 450
        Time  = 482.00 s
        Distribution_sources contains 9 sources
        D + D -> He3 + n(2.45 MeV); Total; P = 136.60 kW
        D + D -> He3 + n(2.45 MeV); Thermal - Thermal; P = 1.57 kW
        D + D -> He3 + n(2.45 MeV); Beam - Thermal; P = 135.03 kW
        D + D -> He3 + n(2.45 MeV); Total; P = -90000000000000011196554993145437224960.00 kW
        D + T -> He4 + n(14.1 MeV); Total; P = 29.37 kW
        D + T -> He4 + n(14.1 MeV); Thermal - Thermal; P = 0.12 kW
        D + T -> He4 + n(14.1 MeV); Beam - Thermal; P = 0.57 kW
        D + T(1 MeV) -> He4 + n(14.1 MeV); Total; P = 29.37 kW
        D + T(1 MeV) -> He4 + n(14.1 MeV); Total; P = -90000000000000011196554993145437224960.00 kW


    .. thumbnail:: _static/images/viewneutron.png
        :alt: image not found
        :align: center

    .. thumbnail:: _static/images/viewneutron2.png
        :alt: image not found
        :align: center