############
 md_summary
############

`md_summary` list available machine description data in a specific
folder with search facility

*******************
 Syntax md_summary
*******************

   .. command-output:: md_summary -h

********************
 Example md_summary
********************

.. code-block:: bash

   $ md_summary  -s 150502/102
   ----> Default call equivalent to:
       md_summary -c pbs,ids,description,backend
   PBS        IDS             DESCRIPTION                                                           BACKEND       SHOT/RUN
   PBS-55.E2  camera_visible  H-alpha view C0 (EP12 left) - Geometry matrix w/o reflections         hdf5          150502/1020
   PBS-55.E2  camera_visible  H-alpha view C0 (EP12 left) - Interpolated geometry matrix at 400 nm  hdf5          150502/1021
   PBS-55.E2  camera_visible  H-alpha view C0 (EP12 left) - Interpolated geometry matrix at 450 nm  hdf5          150502/1022
   PBS-55.E2  camera_visible  H-alpha view C0 (EP12 left) - Interpolated geometry matrix at 500 nm  hdf5          150502/1023
   PBS-55.E2  camera_visible  H-alpha view C0 (EP12 left) - Interpolated geometry matrix at 550 nm  hdf5          150502/1024
   PBS-55.E2  camera_visible  H-alpha view C0 (EP12 left) - Interpolated geometry matrix at 600 nm  hdf5          150502/1025
   PBS-55.E2  camera_visible  H-alpha view C0 (EP12 left) - Interpolated geometry matrix at 650 nm  hdf5          150502/1026
   PBS-55.E2  camera_visible  H-alpha view C0 (EP12 left) - Interpolated geometry matrix at 700 nm  hdf5          150502/1027
   PBS-55.E2  camera_visible  H-alpha - Field of View geometry                                      mdsplus,hdf5  150502/102
   NOTE: Read entry from MD database using user = 'public', database = 'ITER_MD'

.. code-block:: bash

   $ md_summary  -s nbi,on-on
   ----> Default call equivalent to:
       md_summary -c pbs,ids,description,backend
   PBS     IDS  DESCRIPTION                                      BACKEND       SHOT/RUN
   PBS-53  nbi  Heating Neutral Beams (HNB) - HNB1-HNB2 = on-on  mdsplus,hdf5  130000/2501

.. code-block:: bash

   $ md_summary  -s nbi on-on
   ----> Default call equivalent to:
       md_summary -c pbs,ids,description,backend

   PBS   IDS                     DESCRIPTION                        BACKEND      SHOT/RUN
   PBS-53  nbi  Heating Neutral Beams (HNB) - HNB1-HNB2 = off-off  mdsplus,hdf5  130000/2201
   PBS-53  nbi  Heating Neutral Beams (HNB) - HNB1-HNB2 = off-on   mdsplus,hdf5  130000/2301
   PBS-53  nbi  Heating Neutral Beams (HNB) - HNB1-HNB2 = on-off   mdsplus,hdf5  130000/2401
   PBS-53  nbi  Heating Neutral Beams (HNB) - HNB1-HNB2 = on-on    mdsplus,hdf5  130000/2501
   PBS-53  nbi  Diagnostic Neutral Beam (DNB)                      mdsplus,hdf5  130000/3203

   NOTE: Read entry from MD database using user = 'public', database = 'ITER_MD'
