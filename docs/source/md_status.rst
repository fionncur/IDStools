###########
 md_status
###########

`md_status` program provides information about machine description of
specified shot and run number from machine description database. It show
status and potential parent and children for a given simulation stored
in ITER machine description database folder. It helps to see when
particular machine description information become outdated and which one
is in active state.

******************
 Syntax md_status
******************

.. code-block:: bash

   $ md_status -h
   usage: md_status [-h] [-f FOLDER] -s SHOT -r [0-9999]

   ---- Show status and potential parent and children for a given simulation stored in ITER machine description database folder

   optional arguments:
   -h, --help            show this help message and exit
   -f FOLDER, --folder FOLDER
                           folder where to search for machine description data
   -s SHOT, --shot SHOT  shot number
   -r [0-9999], --run [0-9999]
                           run number

*******************
 Example md_status
*******************

.. code-block:: bash

   $ md_status -s 116000 -r 3
   -----------------------------------------------------------------
     DATASET       STATUS          REASON WHY IT REPLACES PREVIOUS
   -----------------------------------------------------------------
     10     2      obsolete        None
     10     3      obsolete        Additional shielding on central column
     116000 1      obsolete        Modified shot number to follow convention
     116000 2      obsolete        Variable reference_temperature added
   * 116000 3      active          Update homogeneous time flag and limiter description
     116000 4      active          Update to match DD v3.40.0
   -----------------------------------------------------------------
