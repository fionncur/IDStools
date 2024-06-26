plothcdwaves
============

*plothcdwaves* shows hcd waveforms

Syntax plothcdwaves
~~~~~~~~~~~~~~~~~~~

   .. command-output:: plothcdwaves -h

Example plothcdwaves
~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ plothcdwaves --uri "imas:mdsplus?user=public;pulse=134173;run=101;database=TEST;version=3"

    .. thumbnail:: _static/images/plothcdwaves.png
        :alt: image not found
        :align: center


    .. code-block:: bash

        $ plothcdwaves --uri "imas:mdsplus?user=schneim;pulse=105039;run=1;database=SAVE;version=3" -t 25

    .. thumbnail:: _static/images/plothcdwaves2.png
        :alt: image not found
        :align: center