########################
 plotmachinedescription
########################

*plotmachinedescription* The plotmachinedescription script is used to visualize 
and plot machine descriptions based on one or more URIs.
It allows users to fetch machine configuration data and display it graphically,
with options to show labels and save figures.

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

   .. image:: _static/images/plotmachinedescription3.png
      :alt: image not found
      :align: center

   .. code-block:: bash

      $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=111001;run=103;database=ITER_MD;version=3#pf_active" --show-labels
      $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=111001;run=103;database=ITER_MD;version=3#pf_active" "imas:mdsplus?user=public;pulse=116000;run=4;database=ITER_MD;version=3#wall" --show-labels
      $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=150100;run=5;database=ITER_MD;version=3#magnetics/flux_loop" --show-labels