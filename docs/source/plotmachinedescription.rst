########################
 plotmachinedescription
########################

*plotmachinedescription* The plotmachinedescription script is used to visualize 
and plot machine descriptions based on one or more URIs.
It allows users to fetch machine configuration data and display it graphically,
with options to show labels and save figures.
You can control visibility of shapes and labels by clicking on legends.

*******************************
 Syntax plotmachinedescription
*******************************

   .. command-output:: plotmachinedescription -h

*********
 Example
*********

   .. code-block:: bash

        $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3"  --show-labels

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
      $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=111001;run=103;database=ITER_MD;version=3#pf_active" 
      "imas:mdsplus?user=public;pulse=116000;run=5;database=ITER_MD;version=3#wall/description_2d[0]/vessel/unit[0:2]" 
      "imas:mdsplus?shot=150100;run=5;user=public;database=ITER_MD;version=3#magnetics" 
      "imas:mdsplus?shot=115004;run=6;user=public;database=ITER_MD;version=3#pf_passive" 
      "imas:mdsplus?user=public;pulse=111002;run=2;database=ITER_MD;version=3#tf" --dd-update
      $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=150100;run=5;database=ITER_MD;version=3#magnetics/flux_loop" --show-labels
      $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=150100;run=5;database=ITER_MD;version=3#magnetics/flux_loop[1:4]" --show-labels
      $ plotmachinedescription --uri "imas:mdsplus?user=public;pulse=116000;run=5;database=ITER_MD;version=3#wall/description_2d[0]/vessel/unit[0:2]" 