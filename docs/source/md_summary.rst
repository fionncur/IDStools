############
 md_summary
############

`md_summary` list available machine description data in a specific
folder with search facility

*******************
 Syntax md_summary
*******************

.. code-block:: bash

   $ md_summary  -h
   usage: md_summary [-h] [-f FOLDER] [-s [SELECTION [SELECTION ...]]] [-o] [-m] [-c CHOICE]

   ---- Script to list available MD data in a specific folder ----

   optional arguments:
   -h, --help            show this help message and exit
   -f FOLDER, --folder FOLDER
                           folder where to search for MD data
   -s [SELECTION [SELECTION ...]], --selection [SELECTION [SELECTION ...]]
                           list of fields to filter: e.g. PBS-55,ece
                           fields listed together (-s A,B) means selecting for both A and B
                           fields listed separately (-s A B) means selecting for either A or B
                           ----> Select only machine description data filling these criteria
   -o, --obsolete        Shows obsolete files
   -m, --matchcase       Match case with selection criteria, default is false
   -c CHOICE, --choice CHOICE
                           list of variables to display, e.g.: pbs,ids,description
                           ... available among following variables:
                                   pbs                    = Plant Breakdown Structure number
                                   ids                    = Name of the IDS
                                   data_provider          = Name of the data provider
                                   data_provider_email    = E-mail of the data provider
                                   ro                     = Name of the diagnostic responsible officer
                                   ro_email               = E-mail of the diagnostic responsible officer
                                   description            = Description of the data
                                   backend                = Backend used to store de IDS
                                   provenance             = Data provenance
                                   status                 = Status of the machine description
                                   replaces               = Old shot/run this one replaces
                                   replaced_by            = Replaced by shot/run
                                   reason_for_replacement = Comment on why this shot/run replaces the previous one

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
