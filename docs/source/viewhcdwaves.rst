viewhcdwaves
============

*viewhcdwaves* shows hcd waveforms

Syntax viewhcdwaves
~~~~~~~~~~~~~~~~~~~

   .. command-output:: viewhcdwaves -h

Example viewhcdwaves
~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ viewhcdwaves -p 134173 -r 101  -d TEST 
        $ viewhcdwaves --uri "imas:mdsplus?user=public;shot=134173;run=101;database=TEST;version=3"

    .. thumbnail:: _static/images/viewhcdwaves.png
        :alt: image not found
        :align: center


    .. code-block:: bash

        $ viewhcdwaves -p 105039 -r 1 -u schneim -d SAVE -t 25

    .. thumbnail:: _static/images/viewhcdwaves2.png
        :alt: image not found
        :align: center