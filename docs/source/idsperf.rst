idsperf
=======

*idsperf* profile performance of access layer operations on dataset.
timing and performance information for different types of operations on
IDS data with the IMAS Python Access Layer

****************
 Syntax idsperf
****************

   .. command-output:: idsperf -h


*****************************
 Example idsperf (all idses)
*****************************

    .. code-block:: bash

        $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" summary
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

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium
      equilibrium best time = 0.6310763321816921 s

********************************************************
 Example idsperf (Show statistics --phowStats --repeat)
********************************************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium --showStats --repeat 2
      All timings  = [0.6093323398381472, 0.5525227133184671]
      Mean         = 0.5809275265783072
      Standard dev = 0.04017047214874087
      Variance     = 0.001613666832652766
      equilibrium best time = 0.5525227133184671 s

****************************************************
 Example idsperf (All slices get_slice performance)
****************************************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium  -a
      equilibrium best time = 0.9812253648415208 s

**********************************************************
 Example idsperf (single SLICETIME get_slice performance)
**********************************************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium  -t 50
      equilibrium best time = 0.022071588784456253 s

*********************************
 Example idsperf (put operation)
*********************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium -do HBD -bo MDSPLUS -o 412
      equilibrium best time = 0.5791653310880065 s

**********************************
 Example idsperf (memory backend)
**********************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium  -t 50 -m
      First import data into memory...
      equilibrium best time = 0.005069989711046219 s
