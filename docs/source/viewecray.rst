###########
 viewecray
###########

*viewecray* shows plots for RF Waves and depositions. This script uses
output of TORBEAM code.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

******************
 Syntax viewecray
******************

   .. command-output:: viewecray -h

*******************
 Example viewecray
*******************

   .. code-block:: bash

        $ viewecray -p 134173 -r 2326  -d TEST 
        $ viewecray --uri "imas:mdsplus?user=public;shot=134173;run=2326;database=TEST;version=3"

   .. image:: _static/images/viewecray.png
      :alt: image not found
      :align: center
