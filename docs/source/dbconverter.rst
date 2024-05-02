#############
 dbconverter
#############

Copy all data-entries from one database into another one

********************
 Syntax dbconverter
********************

    .. command-output:: dbconverter -h
        
*********************
 Example dbconverter
*********************

   .. code:: bash

      $ dbconverter --user <username> --database ITER -do MYDB -bo HDF5
      ----------------------------------------
      Processing (114101, 157)
      Processing... ━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  18% 0:00:51
      successfully converted, backend=MDSPLUS database=MYDB shot=114101 run=157
      ----------------------------------------
      Processing (130011, 1)
      Processing... ━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  18% 0:00:51
      successfully converted, backend=MDSPLUS database=MYDB shot=130011 run=1
      ----------------------------------------
      Processing (130012, 5)
      Processing... ━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  24% 0:00:28
      successfully converted, backend=MDSPLUS database=MYDB shot=130012 run=5
      ----------------------------------------
      Processing (134173, 26)
      Processing... ━━━━━━━━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━  29% 0:00:20
      successfully converted, backend=MDSPLUS database=MYDB shot=134173 run=26
      ----------------------------------------
      Processing (134120, 1)
      Processing... ━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━  41% 0:00:13
      successfully converted, backend=MDSPLUS database=MYDB shot=134120 run=1
      ----------------------------------------
      Processing (123001, 1)
      Processing... ━━━━━━━━━━━━━━━━━━╸━━━━━━━━━━━━━━━━━━━━━  47% 0:00:35
      successfully converted, backend=MDSPLUS database=MYDB shot=123001 run=1

   .. code:: bash

      $ dbconverter --user sawantp1 --database ITER -do MYDB -bo MDSPLUS --validate
      Processing (100027, 1)
      Processing... ━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  12% -:--:--[04/08/24 16:19:45]                                                                                 dbconverter:130
      WARNING:module:could not find schema for core_transport
      Processing... ━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  12% -:--:--[04/08/24 16:19:46]                                                                                     dbconverter:130
      WARNING:module:could not find schema for disruption
      Processing... ━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  12% -:--:--[04/08/24 16:19:49]                                                                                       dbconverter:130
      WARNING:module:could not find schema for pf_active
      Processing... ━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  12% -:--:--[04/08/24 16:19:50]                                                                                      dbconverter:130
      WARNING:module:could not find schema for pf_passive
      Processing... ━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  12% -:--:--[04/08/24 16:19:51]                                                                                            dbconverter:130
      WARNING:module:could not find schema for wall
      Processing... ━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  12% -:--:--
      successfully converted, backend=MDSPLUS database=MYDB shot=100027 run=1
      ----------------------------------------
      Processing (114101, 157)
      Processing... ━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  18% 0:02:17
      successfully converted, backend=MDSPLUS database=MYDB shot=114101 run=157
      ----------------------------------------

      MYDB migration_log--2024_04_08-05:01:40_PM.csv
      134120,1,"[('core_profiles', True, False), ('core_sources', True, 'No Schema'), ('distribution_sources', True, 'No Schema'), ('distributions', True, 'No Schema'), ('waves', True, 'No Schema')]"
      123001,1,"[('equilibrium', True, True)]"
