dbstatus
========

`dbstatus` program provides information about scenario of specified shot and run number from scenario database.
It shows status and potential parent and children for a given simulation stored in ITER scenario description database folder

Syntax dbstatus
~~~~~~~~~~~~~~~

.. code-block:: bash

    $ ddbstatus -h
    usage: dbstatus [-h] [-f FOLDER] -s SHOT -r [0-9999] [--print]

    ---- Show status and potential parent and children for a given simulation stored in ITER database folder

    optional arguments:
    -h, --help            show this help message and exit
    -f FOLDER, --folder FOLDER
                            folder where to search for scenarios
    -s SHOT, --shot SHOT  shot number
    -r [0-9999], --run [0-9999]
                            run number
    --print               print yaml on console



Example dbstatus
~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ dbstatus -s 134174 -r 117
    -----------------------------------------------------------------
     SCENARIO     STATUS     REASON WHY IT REPLACES PREVIOUS
    -----------------------------------------------------------------
     134174  37   obsolete  (134174,7) - DINA, (134102,534) - JINTRAC
     134174  47   obsolete  (134174,37)
     134174  77   obsolete  (134174,47)
     134174  97   obsolete  (134174,77)
     134174  107  obsolete  (134174,97)
    *134174  117  active    (134174,107)
    -----------------------------------------------------------------


.. code-block:: bash

    $ dbstatus -s 130012 -r 4 --print
    {
    │   'status': 'active',
    │   'reference_name': 'ITER-baseline-DT_more_stable_q95>2',
    │   'responsible_name': 'M. Schneider',
    │   'characteristics': {
    │   │   'shot': 130012,
    │   │   'run': 4,
    │   │   'type': 'tbd',
    │   │   'workflow': 'METIS',
    │   │   'machine': 'ITER'
    │   },
    ...
