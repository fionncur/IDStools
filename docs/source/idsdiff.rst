#########
 idsdiff
#########

*idsdiff* script shows ids level differences between two runs. It stores
result in html document. For signals differences it is also shown as
graph.

****************
 Syntax idsdiff
****************

.. code:: bash

   $ idsdiff -h
   usage: idsdiff [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION]
                   [--backendB BACKENDB] [--databaseB DATABASEB] [--userB USERB] [--skip-provenance]
                   [--generate-html] [--report-dir REPORT_DIR]
                   shotA runA shotB runB [ids [ids ...]]

   Compare a IDS from 2 datasets

   positional arguments:
   shotA                 shot number of first dataset
   runA                  run number of first dataset
   shotB                 shot number of second dataset
   runB                  run number of second dataset
   ids                   Name (or space separated list of names) of IDS to compare (leave empty to compare all IDSs)

   optional arguments:
   -h,         --help            show this help message and exit
   -u USER,    --user_or_path USER
                           user (default=public)
   --database DATABASE, -d DATABASE
                           database name (default=ITER)
   --backend BACKEND, -b BACKEND
                           backend format (default=MDSPLUS)
   --version VERSION, -v VERSION
                           data version (default=3)
   --backendB BACKENDB   Specifies the backend of second dataset (default: same as first dataset)
   --databaseB DATABASEB
                           Specifies the database name of second dataset (default: same as first dataset)
   --userB USERB         Specifies the owner (username) of second dataset (default: same as first dataset)
   --skip-provenance     Discards provenance data differences (optional)
   --generate-html       Generate static html page for showing difference including plots
   --report-dir REPORT_DIR
                           Specifies directory where report should be stored

*****************
 Example idsdiff
*****************

   .. code:: bash

      $ idsdiff --generate-html 122525 1 122525 2 summary

   .. image:: _static/images/idsdiff_1.png
      :alt: image not found
      :align: center

   .. image:: _static/images/idsdiff_2.png
      :alt: image not found
      :align: center
