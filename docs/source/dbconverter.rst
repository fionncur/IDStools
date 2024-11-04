#############
 dbconverter
#############

Copy all data-entries from one database to another one. 

********************
 Syntax dbconverter
********************

    .. command-output:: dbconverter -h
        
*********************
 Example dbconverter
*********************

   .. code:: bash

      $ dbconverter --user $USER --database ITER -do MYDB -bo HDF5
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

      $ dbconverter --user $USER --database ITER -do MYDB -bo MDSPLUS --validate
      Processing (100027, 1)
      Processing... ━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  12% -:--:--
      successfully converted, backend=MDSPLUS database=MYDB shot=100027 run=1
      ----------------------------------------
      Processing (114101, 157)
      Processing... ━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  18% 0:02:17
      successfully converted, backend=MDSPLUS database=MYDB shot=114101 run=157
      ----------------------------------------
