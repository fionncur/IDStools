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

        $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3"
         core_profiles best time = 0.6623046789318323 s
         core_sources best time = 1.94440508633852 s
         core_transport best time = 1.0141447838395834 s
         edge_profiles best time = 53.781732397153974 s
         edge_sources best time = 46.661303512752056 s
         edge_transport best time = 42.719197848811746 s
         equilibrium best time = 1.617150105535984 s
         summary best time = 0.11679761670529842 s


***************************
 Example idsperf (one ids)
***************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium
      equilibrium best time = 0.594751663506031 s


********************************************************
 Example idsperf (Show statistics --phowStats --repeat)
********************************************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium --show-stats --repeat 2
      All timings  = [0.6099375672638416, 0.37836710922420025]
      Mean         = 0.49415233824402094
      Standard dev = 0.1637450412023053
      Variance     = 0.026812438518344653
      equilibrium best time = 0.37836710922420025 s


****************************************************
 Example idsperf (All slices get_slice performance)
****************************************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium  -a
      equilibrium best time = 0.6877284124493599 s


**********************************************************
 Example idsperf (single SLICETIME get_slice performance)
**********************************************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium  -t 50
      equilibrium best time = 0.24298583157360554 s


*********************************
 Example idsperf (put operation)
*********************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium --uri-out "imas:mdsplus?user=<username>;pulse=134174;run=412;database=ITER;version=3"
      equilibrium best time = 0.5934083554893732 s

**********************************
 Example idsperf (memory backend)
**********************************

   .. code-block:: bash

      $ idsperf --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" equilibrium  -t 50 -m
      First import data into memory...
      equilibrium best time = 0.003830520436167717 s

