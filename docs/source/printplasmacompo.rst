#################
 printplasmacompo
#################

*printplasmacompo* script gathers ion composition from core and edge
profiles and print it on the screen

************************
 Syntax printplasmacompo
************************

   .. command-output:: printplasmacompo -h
      
*************************
 Example printplasmacompo
*************************

.. code:: bash

   $ printplasmacompo --uri "imas:mdsplus?user=public;pulse=131047;run=4;database=ITER;version=3"
   !   No edge_profiles IDS in the data-entry.
   core +  edge  -
   ------------
   core_profiles
   ------------
   species:      H         D         T         He3       He4       Be        Ne
   a:            1.0       2.0       3.0       3.0       4.0       9.0       20.0
   z:            1.0       1.0       1.0       2.0       2.0       4.0       10.0
   n_over_ntot:  5.29e-06  0.460     0.493     7.01e-07  0.011     0.024     0.012
   n_over_ne:    4.45e-06  0.387     0.414     5.89e-07  9.58e-03  0.020     0.010
   n_over_n_maj: 1.07e-05  0.933     1.000     1.42e-06  0.023     0.048     0.024


.. code:: bash

   $ printplasmacompo --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3"
   14:17:11 INFO     Parsing data dictionary version 3.42.0 @dd_zip.py:166
   14:17:12 INFO     Parsing data dictionary version 3.31.0 @dd_zip.py:166
   ---------------
   core_profiles
   ---------------
   species:                D(D)         T(T)       Be(Be)
   a:                       2.0          3.0          9.0
   z:                       1.0          1.0          4.0
   n_over_ntot:           0.504        0.495     9.53e-04
   n_over_ne:             0.502        0.494     9.51e-04
   n_over_n_maj:          1.000        0.983     1.89e-03
   -----------------------
   D has 1 state
            state1  z : -9e+40     n/ni, % :  100.000000
   T has 1 state
            state1  z : -9e+40     n/ni, % :  100.000000
   Be has 4 states
            state1  z : -9e+40     n/ni, % :    0.000552
            state2  z : -9e+40     n/ni, % :    0.172648
            state3  z : -9e+40     n/ni, % :    0.878612
            state4  z : -9e+40     n/ni, % :   98.948188
   ----------------
   edge_profiles
   ----------------
   core +  edge -