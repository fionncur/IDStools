##################
 plotedgeprofiles
##################

*plotedgeprofiles* script shows edge profiles plots by interpolating on
rectangular grid. It shows Electrons, Ions and Neutral density plots.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*************************
 Syntax plotedgeprofiles
*************************

   .. command-output:: plotedgeprofiles -h


**************************
 Example plotedgeprofiles
**************************

   .. code-block:: bash

        $ plotedgeprofiles --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3" --wall --time 60
        $ plotedgeprofiles --uri "imas:mdsplus?user=public;pulse=123314;run=1;database=ITER;version=3"

   .. image:: _static/images/plotedgeprofiles.png
      :alt: image not found
      :align: center
