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

        $ viewmachinedescription plot wall pf_active 
        23/11/20 23:20:26 WARNING: VS3U : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VS3L : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: TF coil busbars (equivalent coil) : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC1 : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC2 : pf_active.coil.element.geometry.rectangle is empty

   .. thumbnail:: _static/images/machine_description.png
      :alt: image not found
      :align: center

   .. code-block:: bash

      $ viewmachinedescription list pf_active --obsolete
          Pulse |                       IDS Name |                    Status
      --------------------------------------------------------------------------
        111001/1 |                      pf_active |                  obsolete
        111001/2 |                      pf_active |                  obsolete
        111001/3 |                      pf_active |                  obsolete
        111001/4 |                      pf_active |                  obsolete
      111001/101 |                      pf_active |                  obsolete
      111001/201 |                      pf_active |                  obsolete
      111001/102 |                      pf_active |                  obsolete
      111001/202 |                      pf_active |                  obsolete
      111001/103 |                      pf_active |                    active
      111001/203 |                      pf_active |                    active

   .. code-block:: bash

      $ viewmachinedescription list wall pf_active
            Pulse |                       IDS Name |                    Status
      --------------------------------------------------------------------------
       111001/103 |                      pf_active |                    active
       111001/203 |                      pf_active |                    active
         116000/3 |                           wall |                    active
      116100/1001 |                           wall |                    active
      116100/2001 |                           wall |                    active
      116100/3001 |                           wall |                    active
         116612/1 |                           wall |                    active

   .. code-block:: bash

      $ viewmachinedescription plot pf_active wall
      $ viewmachinedescription plot pf_active/111001/103/public/MDSPLUS/ITER_MD/3
      $ viewmachinedescription plot pf_active/111001/103 wall/"imas:mdsplus?user=public;shot=116000;run=4;database=ITER_MD;version=3"