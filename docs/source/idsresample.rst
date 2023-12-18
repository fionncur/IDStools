idsresample
===========

*idsresample* Resample IDSs from a data-entry and save them into another data-entry based on `PREVIOUS_INTERP` method..
more about `imas.imasdef.PREVIOUS_INTERP`:
Interpolation method that returns the previous time slice if the requested time does not exactly exist in the original IDS

Syntax idsresample
~~~~~~~~~~~~~~~~~~

    .. code-block:: bash     

        $ idsresample --help
        Install tqdm to enable progress bar
        usage: idsresample [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -si SHOT_INPUT -ri
                        RUN_INPUT -so SHOT_OUTPUT -ro RUN_OUTPUT [-do DATABASE_OUTPUT] [-bo BACKEND_OUTPUT]
                        [--index-range INDEX_RANGE | --time-range TIME_RANGE]
                        [ids [ids ...]]

        Resample IDSs from a data-entry and save them into another data-entry

        positional arguments:
        ids                   IDSs to resample (leave empty to resample all)

        optional arguments:
        -h, --help            show this help message and exit
        -u USER, --user_or_path USER
                                user (default=sawantp1)
        --database DATABASE, -d DATABASE
                                database name (default=ITER)
        --backend BACKEND, -b BACKEND
                                backend format (default=MDSPLUS)
        --version VERSION, -v VERSION
                                data version (default=3)
        -si SHOT_INPUT, --shot_input SHOT_INPUT
                                Input shot number
        -ri RUN_INPUT, --run_input RUN_INPUT
                                Input run number
        -so SHOT_OUTPUT, --shot_output SHOT_OUTPUT
                                Output shot number
        -ro RUN_OUTPUT, --run_output RUN_OUTPUT
                                Output run number
        -do DATABASE_OUTPUT, --database_output DATABASE_OUTPUT
                                Database name for the destination data-entry
        -bo BACKEND_OUTPUT, --backend_output BACKEND_OUTPUT
                                Backend name for the destination data-entry
        --index-range INDEX_RANGE
                                Specified range of slices index as "start,stop,step". If omitted, start=0,
                                stop=len(timebase),step=1, e.g. "0,,10" to keep 1 every 10 slices. Works only for IDS with
                                homogeneous timebase. (Default)
        --time-range TIME_RANGE
                                Specified range of times as "start,stop,step". If omitted, start=time[0], stop=time[-1]),
                                while omitting step will keep of slices between start and stop, e.g. "10.,50.," to keep all
                                times between 10. and 50. secondes). Works only for IDS with homogeneous timebase unless
                                all three values are specified.


Example idsresample
~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsresample -si 131024 -ri 10 -so 145000 -ro 2
        Install tqdm to enable progress bar
        resampling indices :equilibrium



