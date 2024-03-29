####################
 disruption_summary
####################

Script to list available disruptions in a specific folder

***************************
 Syntax disruption_summary
***************************

.. code-block:: bash

    $ disruption_summary -h
    usage: disruption_summary [-h] [-f FOLDER] [-s SELECTION] [-o] [-c CHOICE]

    ---- Script to list available disruptions in a specific folder ----

    optional arguments:
      -h, --help            show this help message and exit
      -f FOLDER, --folder FOLDER
                            folder where to search for disruptions (recursive)
      -s SELECTION, --selection SELECTION
                            list of fields to filter: e.g. MD,up,2.65
                            ----> Select only disruptions filling these criteria
      -o, --obsolete        Show also obsolete cases
      -c CHOICE, --choice CHOICE
                            list of variables to display, e.g.: shot,run,ip,b0
                            ... available among following variables:
                                    ref_name    = dataset reference name
                                    ro_name     = resonsible officer name
                                    shot        = shot number
                                    run         = run number
                                    type        = data type (experimental,predictive,interpretative)
                                    dis_type    = which type of disruption (MD, VDE...)
                                    VD_dir      = direction of vertical displacement (up, down, central)
                                    HF          = poloidal halo current fraction (HF=Ipol,halo/Ip)
                                    workflow    = suite of codes used to compute these data
                                    database    = database name
                                    ip          = plasma current
                                    IREmax      = maximum RE current
                                    b0          = central magnetic field
                                    ne0         = central electron density
                                    idslist     = List of IDSs available in the data-entry
                                    tsteps      = Number of time steps in the disruptions