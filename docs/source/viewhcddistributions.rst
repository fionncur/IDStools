
viewhcddistributions
====================

*viewhcddistributions* shows waveforms

Syntax viewhcddistributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. command-output:: viewhcddistributions -h


Example viewhcddistributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    .. code-block:: bash

        $ viewhcddistributions -p 130012 -r 115 -d TEST
        $ viewhcddistributions --uri "imas:mdsplus?user=public;shot=130012;run=115;database=TEST;version=3" 

    .. thumbnail:: _static/images/viewhcddistributions2.png
        :alt: image not found
        :align: center

    .. code-block:: bash

        $ viewhcddistributions -p 100015 -r 108 -u schneim -d SPOT
        

    .. thumbnail:: _static/images/viewhcddistributions.png
        :alt: image not found
        :align: center

