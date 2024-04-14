###################
 viewcoretransport
###################

*viewcoretransport* Displays the Core plasma transport of particles,
energy, momentum and poloidal flux.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

**************************
 Syntax viewcoretransport
**************************

   .. code-block:: bash

        $ viewcoretransport -h
        usage: viewcoretransport [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [-m {CLOSEST,PREVIOUS,LINEAR}]
                                [-o OCCURRENCE] [-t TIME] [--save]

      Check match between transport fluxes and a simple calculation

        optional arguments:
        -h, --help            show this help message and exit
        -u USER, --user_or_path USER
                                user            (default=public)
        --database DATABASE, -d DATABASE
                                database name   (default=ITER)
        --backend BACKEND, -b BACKEND
                                backend format  (default=MDSPLUS)
        --version VERSION, -v VERSION
                                data version    (default=3)
        -uri URI, --uri URI   uri             (default=None)
        -s PULSE, --shot PULSE, --pulse PULSE
                                Pulse number
        -r RUN, --run RUN     Run number
        -m {CLOSEST,PREVIOUS,LINEAR}, --slicingmethod {CLOSEST,PREVIOUS,LINEAR}
                                Slicing method  (default=CLOSEST)
        -o OCCURRENCE, --occurrence OCCURRENCE
                                occurrence
        -t TIME, --time TIME  Time
        --save                Save figure at default location

***************************
 Example viewcoretransport
***************************

   .. code-block:: bash

        $ viewcoretransport -d TEST -s 92436 -r 850
        $ viewcoretransport --uri "imas:mdsplus?user=public;shot=92436;run=850;database=TEST;version=3" 

   .. image:: _static/images/viewcoretransport.png
      :alt: image not found
      :align: center
