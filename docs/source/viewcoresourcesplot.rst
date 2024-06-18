#################
 viewcoresourcesplot
#################

*viewcoresourcesplot* plot core sources results.It plots Current, Torque and Particles waveform along with 
Power, particle and current profiles.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

************************
 Syntax viewcoresourcesplot
************************

   .. command-output:: viewcoresourcesplot -h

*************************
 Example viewcoresourcesplot
*************************

   .. code-block:: bash

        $ viewcoresourcesplot --uri "imas:mdsplus?user=public;pulse=130012;run=105;database=TEST;version=3"

    .. thumbnail:: _static/images/viewcoresourcesplot1.png
        :alt: image not found
        :align: center

    .. thumbnail:: _static/images/viewcoresourcesplot2.png
        :alt: image not found
        :align: center


   .. code-block:: bash

        Time  = 190.82 s in range [31.20,328.18] s
        Index = 8
        Averaged resolution = 19.79856 s
        Core_sources contains 1 source
        