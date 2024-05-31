#########
 idsdiff
#########

*idsdiff* script shows ids level differences between two runs. It stores
result in html document. For signals differences it is also shown as
graph.

****************
 Syntax idsdiff
****************

   .. command-output:: idsdiff -h

*****************
 Example idsdiff
*****************


   .. code-block:: bash

      $ idsdiff summary --uri "imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3" "imas:mdsplus?user=public;pulse=122525;run=2;database=ITER;version=3"
      $ idsdiff summary --uri "imas:mdsplus?user=public;pulse=130011;run=6;database=ITER;version=3" "imas:mdsplus?user=public;pulse=130012;run=4;database=ITER;version=3"

   .. thumbnail:: _static/images/idsdiff_1.png
      :alt: image not found
      :align: center

   .. thumbnail:: _static/images/idsdiff_2.png
      :alt: image not found
      :align: center
