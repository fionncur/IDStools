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

    .. command-output:: dblist -h

****************
 Example dblist
****************

.. code-block:: bash

   # Show available databases
   $ dblist databases
   ITER      3
   ITER_MD      3
   TORBEAM      3
   test      3

.. code-block:: bash

   # Show available dataversions with databases from specific user database
   $ dblist -u $USERNAME dataversions
   0 jet_reference
   3        DEBUG         GRAY          HCD         ITER      TORBEAM         

.. code-block:: bash

   # Show available dataversions with databases from specific user database
   $ dblist -u $USERNAME databases
      DEBUG    3
      GRAY     3
      HCD      3
      ITER     3
      TORBEAM  3
      aug      3

.. code-block:: bash

   # Show available time slices with ids names from specific user database
   $ dblist -u $USERNAME slices
   Database: DEBUG
      Data version: 3
         Backend: mdsplus
            Shot 130012
               Run:    26
                        core_profiles:    1 slices (149.98919999999998 - 149.98919999999998)
                        core_sources:    1 slices (149.98919999999998 - 149.98919999999998)
                  distribution_sources:    1 slices (149.98919999999998 - 149.98919999999998)
                        distributions:    1 slices (149.98919999999998 - 149.98919999999998)
                                 waves:    1 slices (149.98919999999998 - 149.98919999999998)
            Shot 134173
               Run:    26

.. code-block:: bash

   # Show available time slices with ids names from specific user database with specific shot/run
   $ dblist -u $USERNAME slices 130012 26
   Database: DEBUG
      Data version: 3
         Backend: mdsplus
            Shot 130012
               Run:    26
                              core_profiles:    1 slices (149.98919999999998 - 149.98919999999998)
                              core_sources:    1 slices (149.98919999999998 - 149.98919999999998)
                        distribution_sources:    1 slices (149.98919999999998 - 149.98919999999998)
                              distributions:    1 slices (149.98919999999998 - 149.98919999999998)
                                       waves:    1 slices (149.98919999999998 - 149.98919999999998)

.. code-block:: bash

   # Show last modified databases with compact output from  specific user database
   dblist -u $USERNAME  list -M -c 
   Database: DEBUG
      Data version: 3
         Backend: mdsplus
            Shot 130012:    1 runs
            Shot 134173:    1 runs
   Database: GRAY
      Data version: 3
         Backend: mdsplus
            Shot      0:    1 runs
            Shot 100000:    1 runs
