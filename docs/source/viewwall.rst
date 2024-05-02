##########
 viewwall
##########

*viewwall* script shows wall outline plot using limiter and vessel
properties found in 2D description of Wall IDS. Here Vessel is
mechanical structure of the vacuum vessel. The script uses annular
represenation. You can specify wall using wall command or you can
specify database entry to retrive wall details. it uses wall ids
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*****************
 Syntax viewwall
*****************

   .. command-output:: viewwall -h

******************
 Example viewwall
******************

   .. code-block:: bash

      $ viewwall wall iter

   .. thumbnail:: _static/images/wallview_iter.png
      :alt: image not found
      :align: center

   .. code-block:: bash

        $ viewwall database -u schneim --database jet -p 92436 -r 271
        $ viewwall database --uri "imas:mdsplus?user=schneim;shot=92436;run=271;database=jet;version=3"

   .. thumbnail:: _static/images/wallview_jet.png
      :alt: image not found
      :align: center
