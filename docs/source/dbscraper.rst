###########
 dbscraper
###########

The *dbscraper* script scrapes data from a particular IDS path for a
specified series of pulses and displays the pulse along with the value.

******************
 dbscraper Syntax
******************

    .. command-output:: dbscraper -h

*******************
 dbscraper Example
*******************

   .. code:: bash

        $ dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --list-count 10
        17:12:15 INFO     Parsing data dictionary version 4.0.0 @dd_zip.py:166
        17:12:15 INFO     Parsing data dictionary version 3.42.0 @dd_zip.py:166
        17:12:20 INFO     Parsing data dictionary version 3.37.1 @dd_zip.py:166
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
        ┃ URI                                                                  ┃ VALUE              ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
        │ "imas:mdsplus?user=public;shot=100020;run=1;database=ITER;version=3" │ 338.51122009888206 │
        ├──────────────────────────────────────────────────────────────────────┼────────────────────┤
        │ "imas:mdsplus?user=public;shot=121024;run=2;database=ITER;version=3" │ 813.9929824799856  │
        ├──────────────────────────────────────────────────────────────────────┼────────────────────┤
        │ "imas:mdsplus?user=public;shot=121024;run=1;database=ITER;version=3" │ 814.9253821062586  │
        ├──────────────────────────────────────────────────────────────────────┼────────────────────┤
        │ "imas:mdsplus?user=public;shot=121024;run=0;database=ITER;version=3" │ 813.7814255877154  │
        ├──────────────────────────────────────────────────────────────────────┼────────────────────┤
        │ "imas:mdsplus?user=public;shot=104010;run=5;database=ITER;version=3" │ 813.2177299361855  │
        ├──────────────────────────────────────────────────────────────────────┼────────────────────┤
        │ "imas:mdsplus?user=public;shot=105009;run=8;database=ITER;version=3" │ 0.0                │
        ├──────────────────────────────────────────────────────────────────────┼────────────────────┤
        │ "imas:mdsplus?user=public;shot=135008;run=6;database=ITER;version=3" │ 807.75             │
        ├──────────────────────────────────────────────────────────────────────┼────────────────────┤
        │ "imas:mdsplus?user=public;shot=115002;run=6;database=ITER;version=3" │ 0.0                │
        ├──────────────────────────────────────────────────────────────────────┼────────────────────┤
        │ "imas:mdsplus?user=public;shot=131052;run=1;database=ITER;version=3" │ 811.6077264479162  │
        ├──────────────────────────────────────────────────────────────────────┼────────────────────┤
        │ "imas:mdsplus?user=public;shot=131052;run=0;database=ITER;version=3" │ 810.605443560561   │
        └──────────────────────────────────────────────────────────────────────┴────────────────────┘

