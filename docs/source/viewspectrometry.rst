viewspectrometry
================

*viewspectrometry* Display the spectrum from spectrometer_visible idses. It shows plots of radiance and intensity of the spectrom in two different windows.


Syntax viewspectrometry
~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash   

        $ viewspectrometry -h
        usage: viewspectrometry [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [-t TIME] [--save]

        ---- Display spectrum from spectrometer_visible

        optional arguments:
        -h, --help            show this help message and exit
        -u USER, --user_or_path USER
                                user (default=public)
        --database DATABASE, -d DATABASE
                                database name (default=ITER)
        --backend BACKEND, -b BACKEND
                                backend format (default=MDSPLUS)
        --version VERSION, -v VERSION
                                data version (default=3)
        -uri URI, --uri URI   uri (default=None)
        -s PULSE, --shot PULSE, --pulse PULSE
                                Pulse number
        -r RUN, --run RUN     Run number
        -t TIME, --time TIME  Time
        --save                Save figure at default location


Example 
~~~~~~~

    .. code-block:: bash

        $ viewspectrometry -d TEST -s 134000 -r 37
        $ viewspectrometry --uri "imas:mdsplus?user=public;shot=134000;run=37;database=TEST;version=3"


    .. image:: _static/images/viewspectrometry.png
        :alt: image not found
        :align: center






