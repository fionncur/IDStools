##################
 viewedgeprofiles
##################

*viewedgeprofiles* script shows edge profiles plots by interpolating on
rectangular grid. It shows Electrons, Ions and Neutral density plots.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*************************
 Syntax viewedgeprofiles
*************************

   .. command-output:: viewedgeprofiles -h


**************************
 Example viewedgeprofiles
**************************

   .. code-block:: bash

        $ viewedgeprofiles -p 123314 -r 1 --separatix --wall
        $ viewedgeprofiles --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" --separatix --wall --time 60

   .. image:: _static/images/viewedgeprofiles.png
      :alt: image not found
      :align: center
