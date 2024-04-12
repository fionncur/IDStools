#########
 idsperf
#########

*idsperf* profile performance of access layer operations on dataset.
timing and performance information for different types of operations on
IDS data with the IMAS Python Access Layer

****************
 Syntax idsperf
****************

   .. code-block:: bash

      $ idsperf -h
      usage: idsperf [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-t SLICETIME [SLICETIME ...] | -a] [-m] [-do DATABASE_OUTPUT]
                  [-bo BACKEND_OUTPUT] [--repeat REPEAT] [--verbose] [--showStats] [--profile] [-o OUTPUTRUN] -s SHOT -r RUN
                  [ids [ids ...]]

      This script gives simple timing and performance information for different types of operations on IDS data with the IMAS Python Access Layer (get/get_slice/put
      depending on selected options)

      positional arguments:
      ids                   IDS name(s) (leave empty to select all IDSs with default occurrence, or append "/n" to copy a specific occurrence "n")

      optional arguments:
      -h, --help            show this help message and exit
      -u USER, --user_or_path USER
                              user (default=public)
      --database DATABASE, -d DATABASE
                              database name (default=ITER)
      --backend BACKEND, -b BACKEND
                              backend format (default=MDSPLUS)
      --version VERSION, -v VERSION
                              data version (default=3)
      -t SLICETIME [SLICETIME ...], --sliceTime SLICETIME [SLICETIME ...]
                              Use get_slice with selected time(s)
      -a, --allSlices       Use get_slice with all available times
      -m, --memoryBackend   Use MEMORY_BACKEND for this test (involve reading from file and loading in memory first)
      -do DATABASE_OUTPUT, --database_output DATABASE_OUTPUT
                              Database name for the destination data-entry
      -bo BACKEND_OUTPUT, --backend_output BACKEND_OUTPUT
                              Backend name for the destination data-entry
      --repeat REPEAT       Repeat timing n times (default: 1)
      --verbose             Verbose mode, prints additional information
      --showStats           Print addition stats for timings
      --profile             Also do full profile of the selected operation, via cProfile
      -o OUTPUTRUN, --outputRun OUTPUTRUN
                              Output run number for checking perf of put
      -s SHOT, --shot SHOT  Shot number
      -r RUN, --run RUN     Run number

*****************************
 Example idsperf (all idses)
*****************************

   .. code-block:: bash

      $ idsperf -s 134174 -r 117
      core_profiles best time = 1.0308142956346273 s
      core_sources best time = 2.8891310710459948 s
      core_transport best time = 1.7229742156341672 s
      edge_profiles best time = 111.6962537476793 s
      edge_sources best time = 88.04306311160326 s
      edge_transport best time = 69.34100596047938 s
      equilibrium best time = 0.6164609286934137 s
      summary best time = 0.1234514331

***************************
 Example idsperf (one ids)
***************************

   .. code-block:: bash

      $ idsperf -s 134174 -r 117 equilibrium
      equilibrium best time = 0.6310763321816921 s

********************************************************
 Example idsperf (Show statistics --showStats --repeat)
********************************************************

   .. code-block:: bash

      $ idsperf -s 134174 -r 117 equilibrium --showStats --repeat 2
      All timings  = [0.6093323398381472, 0.5525227133184671]
      Mean         = 0.5809275265783072
      Standard dev = 0.04017047214874087
      Variance     = 0.001613666832652766
      equilibrium best time = 0.5525227133184671 s

****************************************************
 Example idsperf (All slices get_slice performance)
****************************************************

   .. code-block:: bash

      $ idsperf -s 134174 -r 117 equilibrium  -a
      equilibrium best time = 0.9812253648415208 s

**********************************************************
 Example idsperf (single SLICETIME get_slice performance)
**********************************************************

   .. code-block:: bash

      $ idsperf -s 134174 -r 117 equilibrium  -t 50
      equilibrium best time = 0.022071588784456253 s

*********************************
 Example idsperf (put operation)
*********************************

   .. code-block:: bash

      $ idsperf -s 134174 -r 117 equilibrium -do HBD -bo MDSPLUS -o 412
      equilibrium best time = 0.5791653310880065 s

**********************************
 Example idsperf (memory backend)
**********************************

   .. code-block:: bash

      $ idsperf -s 134174 -r 117 equilibrium  -t 50 -m
      First import data into memory...
      equilibrium best time = 0.005069989711046219 s
