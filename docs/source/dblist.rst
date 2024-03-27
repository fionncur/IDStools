########
 dblist
########

This program lists existing IMAS databases.

Possible commands are: list <shot number>- list existing databases
slices <shot number> <run number> - list existing databases, including
number of timeslices and time range for time-dependent IDSs times <shot
number> <run number> - list existing databases, including number of
timeslices their time points for time-dependent IDSs databases - list
existing databases (with data versions) dataversions - list existing
dataversions (with databases)

If the optional arguments shot number and run number are given, only
databases with these numbers will be shown.

If no command is given, the list command is performed.

To see databases stored in the public imas database, use 'public' as the
user name.

***************
 Syntax dblist
***************

.. code-block:: bash

   $ dblist
   usage: dblist [-h] [-u USER] [-d DATABASE] [-v VERSION] [--backend BACKEND]
               {list,slices,times,databases,dataversions} ... [positionalArgs]

   [Previously known as imasdbs]


   positional arguments:
   {list,slices,times,databases,dataversions}
                           sub-commands help
       list                list databases
       slices              list slices
       times               list times
       databases           print databases
       dataversions        print data versions
   positionalArgs

   optional arguments:
   -h, --help            show this help message and exit
   -u USER, --user USER  Show databases of specified user (default=sawantp1)
   -d DATABASE, --database DATABASE
                           Show only databases with specified name (default=None)
   -v VERSION, --version VERSION
                           Show only databases for specified major data version (default=None)
   --backend BACKEND     Show databases written with given backend(s). Comma-separated list of backends (Currently
                           supported: mdsplus, hdf5). By default all backends are shown. (default=None)

****************
 Example dblist
****************

.. code-block:: bash

   $ dblist databases
   ITER      3
   ITER_MD      3
   TORBEAM      3
   test      3
