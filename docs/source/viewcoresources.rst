#################
 viewcoresources
#################

*viewcoresources* plot core sources results.It plots Current, Torque and Particles waveform along with 
Power, particle and current profiles.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

************************
 Syntax viewcoresources
************************

   .. command-output:: viewcoresources -h

*************************
 Example viewcoresources
*************************

   .. code-block:: bash

        $ viewcoresources -p 130012 -r 105 -d TEST
        $ viewcoresources --uri "imas:mdsplus?user=public;shot=130012;run=105;database=TEST;version=3"
        Time  = 190.82 s in range [31.20,328.18] s
        Index = 8
        Averaged resolution = 19.79856 s
        Core_sources contains 1 source
        

    .. thumbnail:: _static/images/viewcoresources.png
        :alt: image not found
        :align: center

