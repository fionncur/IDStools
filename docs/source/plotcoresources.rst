#################
 plotcoresources
#################

*plotcoresources* plot core sources results.It plots Current, Torque and Particles waveform along with 
Power, particle and current profiles.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

************************
 Syntax plotcoresources
************************

    .. command-output:: plotcoresources -h

*************************
 Example plotcoresources
*************************

    .. code-block:: bash

        $ plotcoresources --uri "imas:mdsplus?user=public;pulse=130012;run=105;database=TEST;version=3"
        Time  = 190.82 s in range [31.20,328.18] s
        Index = 8
        Averaged resolution = 19.79856 s
        Core_sources contains 1 source


    .. image:: _static/images/plotcoresources.png
        :alt: image not found
        :align: center