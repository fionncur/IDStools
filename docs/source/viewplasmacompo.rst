#################
 viewplasmacompo
#################

*viewplasmacompo* script gathers ion composition from core and edge
profiles and print it on the screen

************************
 Syntax viewplasmacompo
************************

   .. command-output:: viewplasmacompo -h
      
*************************
 Example viewplasmacompo
*************************

.. code:: bash

   $ viewplasmacompo -p 131047 -r 4
   $ viewplasmacompo --uri "imas:mdsplus?user=public;shot=131047;run=4;database=ITER;version=3"
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
