###########
 plotecray
###########

*plotecray* shows plots for RF Waves and depositions. This script uses
output of TORBEAM code.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

******************
 Syntax plotecray
******************

   .. command-output:: plotecray -h

*******************
 Example plotecray
*******************

   .. code-block:: bash

        $ plotecray --uri "imas:mdsplus?user=public;pulse=134173;run=2326;database=TEST;version=3" -md wall

   .. image:: _static/images/plotecray.png
      :alt: image not found
      :align: center
