########################
 plotmachinedescription
########################

*plotmachinedescription* lists machine description data entries 
Plots machine description data 
Retrieve machine description from yaml file
plotmachinedescription plot pf_active wall

Specify particular data entry with optional format <idsname>/pulse/run/user/backend/database/version
plotmachinedescription plot <idsname>/pulse/run/user/backend/database/version

Specify URI 
plotmachinedescription plot pf_active/111001/103 wall/"imas:mdsplus?user=public;pulse=116000;run=4;database=ITER_MD;version=3"
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*******************************
 Syntax plotmachinedescription
*******************************

   .. command-output:: plotmachinedescription -h

*********
 Example
*********

   .. code-block:: bash

        $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3"  --show-labels
        23/11/20 23:20:26 WARNING: VS3U : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VS3L : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: TF coil busbars (equivalent coil) : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC1 : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC2 : pf_active.coil.element.geometry.rectangle is empty

   .. image:: _static/images/plotmachinedescription.png
      :alt: image not found
      :align: center

   .. image:: _static/images/plotmachinedescription2.png
      :alt: image not found
      :align: center

   .. code-block:: bash

      $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=111001;run=103;database=ITER_MD;version=3#pf_active" --show-labels
      $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=111001;run=103;database=ITER_MD;version=3#pf_active" "imas:mdsplus?user=public;pulse=116000;run=4;database=ITER_MD;version=3#wall" --show-labels