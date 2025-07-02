###########
 dbscraper
###########

The *dbscraper* script scrapes data from a particular IDS path for a
specified series of pulses and displays the pulse along with the value.
The *dbscraper* script is a tool designed to extract and display data from IDS 
paths across multiple pulses. It allows users to query specific data elements 
and apply filtering conditions to the results.

The script supports:
- Accessing data at specific IDS paths
- Limiting the number of results with `--list-count`
- Filtering data using simple expressions via the `--query` parameter
- Handling both scalar and array data
- Retrieving data from multiple paths simultaneously you can provide multiple ids paths
- Performing complex operations on retrieved data, such as finding maximum values or applying conditional logic

These capabilities make dbscraper particularly useful for quick data exploration, comparing values across multiple pulses,
and identifying pulses with specific characteristics of interest.

******************
 dbscraper Syntax
******************

    .. command-output:: dbscraper -h

*******************
 dbscraper Example
*******************

   .. code:: bash

        $ dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --list-count 10
        11:50:55 INFO     Parsing data dictionary version 4.0.0 @dd_zip.py:89
        11:50:56 INFO     Parsing data dictionary version 3.42.0 @dd_zip.py:89
        11:50:57 INFO     Parsing data dictionary version 3.37.1 @dd_zip.py:89
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ URI                                                                ┃ equilibrium/time_slice(0)/global_quantities/volume ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ imas:mdsplus?user=public;shot=100020;run=1;database=ITER;version=3 │ 338.51122009888206                                 │
        ├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=121024;run=2;database=ITER;version=3 │ 813.9929824799856                                  │
        ├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=121024;run=1;database=ITER;version=3 │ 814.9253821062586                                  │
        ├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=121024;run=0;database=ITER;version=3 │ 813.7814255877154                                  │
        ├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=104010;run=5;database=ITER;version=3 │ 813.2177299361855                                  │
        ├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=105009;run=8;database=ITER;version=3 │ 0.0                                                │
        ├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=135008;run=6;database=ITER;version=3 │ 807.75                                             │
        ├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=115002;run=6;database=ITER;version=3 │ 0.0                                                │
        ├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=131052;run=1;database=ITER;version=3 │ 811.6077264479162                                  │
        ├────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=131052;run=0;database=ITER;version=3 │ 810.605443560561                                   │
        └────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────┘
        
        $ dbscraper "ec_launchers/beam(:)/power_launched/data" "ec_launchers/beam(:)/launching_position/r" --list-count 1 --query "np.any(x1.flatten() > 1000.0) and np.any(x2.flatten() < 8)"
        11:51:54 INFO     Parsing data dictionary version 4.0.0 @dd_zip.py:89
        11:51:55 INFO     Parsing data dictionary version 3.25.0 @dd_zip.py:89
        11:51:56 INFO     Parsing data dictionary version 3.41.0 @dd_zip.py:89
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ URI                                                        ┃ ec_launchers/beam(:)/power_launched/data ┃ ec_launchers/beam(:)/launching_position/r ┃ np.any(x1.flatten() > 1000.0) and np.any(x2.flatten() < 8) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ imas:mdsplus?user=public;shot=130012;run=5;database=ITER;v │ (56, 1) array (mean=357000.00)           │ (56, 1) array (mean=8.29)                 │ True                                                       │
        │ ersion=3                                                   │                                          │                                           │                                                            │
        └────────────────────────────────────────────────────────────┴──────────────────────────────────────────┴───────────────────────────────────────────┴────────────────────────────────────────────────────────────┘

        $ dbscraper "summary/global_quantities/ip/value" --list-count 5 --query "np.max(np.abs(x1)) > 5000000 and np.max(np.abs(x1)) < 7500000"
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                                        ┃                                         ┃ np.max(np.abs(x1)) > 5000000 and       ┃
        ┃ URI                                    ┃ summary/global_quantities/ip/value      ┃ np.max(np.abs(x1)) < 7500000           ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ imas:mdsplus?user=public;shot=103034;r │ <IDSNumericArray (IDS:summary,          │ True                                   │
        │ un=3;database=ITER;version=3           │ global_quantities/ip/value, FLT_1D)>    │                                        │
        │                                        │ numpy.ndarray([-5107787.292])           │                                        │
        ├────────────────────────────────────────┼─────────────────────────────────────────┼────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=103047;r │ <IDSNumericArray (IDS:summary,          │ True                                   │
        │ un=3;database=ITER;version=3           │ global_quantities/ip/value, FLT_1D)>    │                                        │
        │                                        │ numpy.ndarray([-5107787.292])           │                                        │
        ├────────────────────────────────────────┼─────────────────────────────────────────┼────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=103055;r │ <IDSNumericArray (IDS:summary,          │ True                                   │
        │ un=3;database=ITER;version=3           │ global_quantities/ip/value, FLT_1D)>    │                                        │
        │                                        │ numpy.ndarray([-5107787.292])           │                                        │
        ├────────────────────────────────────────┼─────────────────────────────────────────┼────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=103033;r │ <IDSNumericArray (IDS:summary,          │ True                                   │
        │ un=3;database=ITER;version=3           │ global_quantities/ip/value, FLT_1D)>    │                                        │
        │                                        │ numpy.ndarray([-5107787.292])           │                                        │
        ├────────────────────────────────────────┼─────────────────────────────────────────┼────────────────────────────────────────┤
        │ imas:mdsplus?user=public;shot=103042;r │ <IDSNumericArray (IDS:summary,          │ True                                   │
        │ un=3;database=ITER;version=3           │ global_quantities/ip/value, FLT_1D)>    │                                        │
        │                                        │ numpy.ndarray([-5107787.292])           │                                        │
        └────────────────────────────────────────┴─────────────────────────────────────────┴────────────────────────────────────────┘

        # List data entries which has D+ ion density values
        $ dbscraper "core_profiles/profiles_1d(0)/ion(:)/label" --list-count 5 --query "'D+' in x1"

        # List data entries where the volume is greater than 800
        $ dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --list-count 5 --query "x1 > 800"

        # List data entries where the maximum value of the ion density is less than -5,000,000
        $ dbscraper "summary/global_quantities/ip/value" --list-count 50 --query "np.max(x1) < -5000000.0"

        # List data entries where the electron temperature is greater than 10,000 eV
        $ dbscraper "core_profiles/profiles_1d(:)/electrons/temperature[0]" --list-count 5 --query "np.mean(x1) > 10000"
        
        # List data entries where the electron temperature is less than 10,000 eV
        $ dbscraper "core_profiles/profiles_1d(0)/electrons/temperature" --list-count 5 --query "np.abs(x1) < 10000"

        # Get pulses with maximum ion density for D+ ions
        $ dbscraper "core_profiles/profiles_1d(0)/ion(:)/label" "core_profiles/profiles_1d(0)/ion(:)/density" --list-count 1 --query "x1[np.argmax(np.max(x2, axis=1))] == 'D+'"
