########################
 viewmachinedescription
########################

*viewmachinedescription* lists machine description data entries 
Plots machine description data 
Retrieve machine description from yaml file
viewmachinedescription plot pf_active wall

Specify particular data entry with optional format <idsname>/pulse/run/user/backend/database/version
viewmachinedescription plot <idsname>/pulse/run/user/backend/database/version

Specify URI 
viewmachinedescription plot pf_active/111001/103 wall/"imas:mdsplus?user=public;shot=116000;run=4;database=ITER_MD;version=3"
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*******************************
 Syntax viewmachinedescription
*******************************

   .. command-output:: viewmachinedescription -h

*********
 Example
*********

   .. code-block:: bash

        $ viewmachinedescription -mdesc wall pf_active 
        23/11/20 23:20:26 WARNING: VS3U : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VS3L : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: TF coil busbars (equivalent coil) : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC1 : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC2 : pf_active.coil.element.geometry.rectangle is empty

   .. thumbnail:: _static/images/machine_description.png
      :alt: image not found
      :align: center

   .. code-block:: bash

      $ viewmachinedescription -mdesc pf_active wall
      $ viewmachinedescription -mdesc "imas:mdsplus?user=public;shot=111001;run=103;database=ITER_MD;version=3#pf_active"
      $ viewmachinedescription -mdesc "imas:mdsplus?user=public;shot=111001;run=103;database=ITER_MD;version=3#pf_active" "imas:mdsplus?user=public;shot=116000;run=4;database=ITER_MD;version=3#wall"