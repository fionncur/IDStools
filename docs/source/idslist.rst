#########
 idslist
#########

*idslist* is a utility that, as the name implies, shows list of all
idses along with count of time slices. It also shows timestamps of
slices. You can customize the output by choosing to display full array
values or generate output in YAML format.

****************
 Syntax idslist
****************

   .. command-output:: idslist -h



Example idslist
~~~~~~~~~~~~~~~~

   .. code-block:: bash

        $ idslist --uri "imas:mdsplus?user=public;pulse=122481;run=1;database=ITER;version=3"

                        List of IDSes                  
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━┓
        ┃ IDS                 ┃ SLICES ┃ TIME          ┃
        ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━┩
        │ dataset_description │ 1      │ array([0.04]) │
        │ edge_profiles       │ 1      │ array([0.04]) │
        │ edge_sources        │ 1      │ array([0.04]) │
        │ edge_transport      │ 1      │ array([0.04]) │
        │ equilibrium         │ 1      │ array([0.])   │
        │ radiation           │ 1      │ array([0.04]) │
        │ summary             │ 1      │ array([0.04]) │
        │ wall                │ 1      │ array([0.])   │
        └─────────────────────┴────────┴───────────────┘



   .. code-block:: bash

        # Show idses with their occurrences and comment
        $ idslist --uri "imas:mdsplus?user=public;pulse=122481;run=1;database=ITER;version=3" -c
                                                                List of IDSes with Occurrences                                                         
        ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ IDS                   ┃ COMMENT                                                                                                             ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ dataset_description/0 │ b2mn     B2.5 bjb99/7 SOLPS-ITER  2020-06-03  21:34 bonninx ITER#2481_(F57-100-Ne_1.8%-Be0,_tau=0.33e-6,_ntime=150) │
        │ edge_profiles/0       │ b2mn     B2.5 bjb99/7 SOLPS-ITER  2020-06-03  21:34 bonninx ITER#2481_(F57-100-Ne_1.8%-Be0,_tau=0.33e-6,_ntime=150) │
        │ edge_sources/0        │ b2mn     B2.5 bjb99/7 SOLPS-ITER  2020-06-03  21:34 bonninx ITER#2481_(F57-100-Ne_1.8%-Be0,_tau=0.33e-6,_ntime=150) │
        │ edge_transport/0      │ b2mn     B2.5 bjb99/7 SOLPS-ITER  2020-06-03  21:34 bonninx ITER#2481_(F57-100-Ne_1.8%-Be0,_tau=0.33e-6,_ntime=150) │
        │ equilibrium/0         │                                                                                                                     │
        │ radiation/0           │ b2mn     B2.5 bjb99/7 SOLPS-ITER  2020-06-03  21:34 bonninx ITER#2481_(F57-100-Ne_1.8%-Be0,_tau=0.33e-6,_ntime=150) │
        │ summary/0             │ b2mn     B2.5 bjb99/7 SOLPS-ITER  2020-06-03  21:34 bonninx ITER#2481_(F57-100-Ne_1.8%-Be0,_tau=0.33e-6,_ntime=150) │
        │ wall/0                │ DivGeo template                                                                                                     │
        └───────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘


   .. code-block:: bash

        $ idslist --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" -y
        core_profiles:
            time_step_number: 106
            start_end_step:   [10.599230769230868 75.00005602665553 0.6133411929278538]
        core_sources:
            time_step_number: 106
            start_end_step:   [10.599230769230868 75.00005602665553 0.6133411929278538]
        core_transport:
            time_step_number: 106
            start_end_step:   [10.599230769230868 75.00005602665553 0.6133411929278538]
        edge_profiles:
            time_step_number: 650
            start_end_step:   [10.1 75.0 0.1]
        edge_sources:
            time_step_number: 650
            start_end_step:   [10.1 75.0 0.1]
        edge_transport:
            time_step_number: 650
            start_end_step:   [10.1 75.0 0.1]
        equilibrium:
            time_step_number: 106
            start_end_step:   [1.202 149.43759781205512 1.4117675982100488]
        summary:
            time_step_number: 106
            start_end_step:   [10.299692307692405 75.00005602665553 0.6161939401806011]

   .. code-block:: bash

        # Show full time array
        $ idslist --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" -f
        14:58:37 INFO     Parsing data dictionary version 3.42.0 @dd_zip.py:166
        14:58:37 INFO     Parsing data dictionary version 3.31.0 @dd_zip.py:166
                                                                        List of IDSes                                                                   
        ┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ IDS            ┃ SLICES ┃ TIME                                                                                                                 ┃
        ┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ core_profiles  │ 106    │ array([10.5992, 10.5992, 10.5992, 10.5992, 10.5992, 10.5992, 10.5992, 10.5992, 10.5992, 10.5992, 10.5992, 10.5992,   │
        │                │        │ 10.5992, 11.4376, 12.9376, 14.4376, 15.9376, 17.4376, 18.9376, 20.4376, 21.9376, 23.4376, 24.9376, 26.4376, 27.9376, │
        │                │        │ 29.4376, 30.9376, 32.4376, 33.9376, 35.4376, 36.9376, 38.4376, 39.9376, 41.4376, 42.9376, 44.4376, 45.9376, 47.4376, │
        │                │        │ 48.9376, 50.4376, 51.9376, 53.4376, 54.9376, 56.4376, 57.9376, 59.4376, 60.9376, 62.4376, 63.9376, 65.4376, 66.9376, │
        │                │        │ 68.4376, 69.9376, 71.4376, 72.9376, 74.4376, 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , │
        │                │        │ 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , │
        │                │        │ 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , │
        │                │        │ 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.    , 75.0001, 75.0001, 75.0001, 75.0001, │
        │                │        │ 75.0001, 75.0001, 75.0001])   