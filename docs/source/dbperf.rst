dbperf
======

*dbperf* evaluates performance of MDSPLUS and HDF5 Backends with IDS get operation


Syntax dbperf
~~~~~~~~~~~~~~~

    .. code-block:: bash   

        $ dbperf -h
        Usage: dbperf [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-md MDSDATABASE] [-mdu MDSUSER] [-hd HDF5DATABASE] [-hdu HDF5USER]
                    [-f FILE] [-p PULSE] [--run RUN] [--ids [IDS [IDS ...]]] [-rep REPEAT] [-excp [EXCLUDEP [EXCLUDEP ...]]] [-exci [EXCLUDEIDS [EXCLUDEIDS ...]]]
                    [-rot ROTATION] [-fw FONTWEIGHT] [-siz] [-xlog] [-ylog] [-sli] [-tim] [--idsperf] [--avgdf] [-verb]

        Times IDS getting of given Pulse and Run, contrasts with IDS size and slices. replaced by db_backend_benchmark.py

        Optional Arguments:
        -h, --help            show this help message and exit
        -u, --user_or_path USER
                                user (default=public)
        --database, -d DATABASE
                                database name (default=ITER)
        --backend, -b BACKEND
                                backend format (default=MDSPLUS)
        --version, -v VERSION
                                data version (default=3)
        -md, --mdsdatabase MDSDATABASE
                                Path to database in MDSPLUS (if separate to HDF5)
        -mdu, --mdsuser MDSUSER
                                User harboring database in MDSPLUS (if separate to HDF5)
        -hd, --hdf5database HDF5DATABASE
                                Path to database in HDF5 (if separate to MDSPLUS)
        -hdu, --hdf5user HDF5USER
                                User harboring database in HDF5 (if separate to MDSPLUS)
        -f, --file FILE       Path to already generated .csv file with backend performances
        -p, --pulse PULSE     Pulse number harboring desired IDSs
        --run RUN             Run number harboring desired IDSs
        --ids [IDS [IDS ...]]
                                IDS to test and/or plot
        -rep, --repeat REPEAT
                                Number of times IDS get should be performed
        -excp, --excludep [EXCLUDEP [EXCLUDEP ...]]
                                Tuple of Pulse and Runs to exclude
        -exci, --excludeids [EXCLUDEIDS [EXCLUDEIDS ...]]
                                IDS(s) to exclude
        -rot, --rotation ROTATION
                                Number of degrees to tilt IDS names on x-axis (default=90)
        -fw, --fontweight FONTWEIGHT
                                Fontweight for plot axes (options include: 'ultralight', 'light', 'normal', 'bold', 'heavy') (default='bold')
        -siz, --sizevtime     Evaluate performance based on time taken to read IDS size in MB
        -xlog, --xlogscale    Scale x-axis with logscale
        -ylog, --ylogscale    Scale y-axis with logscale
        -sli, --slicevtime    Evaluate performance based on time taken to read number of IDS slices
        -tim, --time          Evaluate performance based on time taken to read an IDS
        --idsperf             Display performance of individual IDSs on all measured runs
        --avgdf               Return dataframe and consequent plots of measured values' averages in evaluated pulse(s)
        -verb, --verbose      Verbose mode for printing used pulses and dataframes


Example dbperf
~~~~~~~~~~~~~~

    .. code-block:: bash

        $ dbperf -u <username> -d ITER
