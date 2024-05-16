#####################
 IDStools Cheatsheet
#####################

This cheat sheet provides quick references for commonly used commands in
IDStools. :download:`download cheatsheet here <_static/cheatsheet.pdf>`


****************
 Analysis Tools
****************

+----------------------------+--------------------------------------------------------------+
| Command                    | Description and Example Usage                                |
+============================+==============================================================+
|``viewcoresources``         | Plots core_sources results (replaces csplot).                |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewcoresources -p 130012 -r 5 -d TEST                  |
+----------------------------+--------------------------------------------------------------+
| ``viewcoretransport``      | Core plasma transport of particles, energy,                  |
|                            | momentum and poloidal flux (replaces check_transport).       |
|                            |                                                              |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewcoretransport -u public -d TEST -p 92436 -r 850     |
|                            |                                                              |
+----------------------------+--------------------------------------------------------------+
|``vieweccomposition``       | Display ec results (replaces eccomp).                        |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ vieweccomposition -d TEST -p 134173 -r 2326             |
+----------------------------+--------------------------------------------------------------+
|``viewecray``               | Display EC wave ray-tracing results (replaces ecray).        |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewecray -d TEST -p 134173 -r 2326                     |
+----------------------------+--------------------------------------------------------------+
|``viewecstrayradiation``    | Shows electron cyclotron stray radiation.                    |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewecstrayradiation -p 134174 -r 117                   |
+----------------------------+--------------------------------------------------------------+
| ``viewedgeprofiles``       | Shows edge profiles plots by interpolating on rectangular    |
|                            | grid.                                                        |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewedgeprofiles -p 123314 -r 1 --separatix --wall      |
+----------------------------+--------------------------------------------------------------+
| ``viewequilibrium``        | Shows plasma equilibrium  (replaces equiplot).               |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewequilibrium -p 134174 -r 117 --rho --pfcoils --info |
+----------------------------+--------------------------------------------------------------+
| ``viewfluxes``             | Shows flux information from available                        |
|                            | transport models  (replaces print_fluxes).                   |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewfluxes -p 134174 -r  117 -m CLOSEST                 |
+----------------------------+--------------------------------------------------------------+
| ``viewhcddistributions``   | shows waveforms  (replaces hcd_distributions_plot).          |
|                            |                                                              |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewhcddistributions -p 130012 -r 115 -d TEST           |
+----------------------------+--------------------------------------------------------------+
| ``viewhcdplots``           | shows plots from distributions and waves for                 |
|                            | different data entries for analysis   (replaces hcd_plot).   |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewhcdplots  -ech 134173/101/public/MDSPLUS/TEST/3     |
|                            |    -nbi 130012/115/public/MDSPLUS/TEST/3                     |
|                            |    -fus 130012/115/public/MDSPLUS/TEST/3                     |
|                            |    -icrh 130012/15/public/MDSPLUS/TEST/3                     |
+----------------------------+--------------------------------------------------------------+
| ``viewhcdwaves``           | shows waveforms  (replaces hcd_waves_plot).                  |
|                            |                                                              |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewhcdwaves -p 134173 -r 101 -d TEST                   |
+----------------------------+--------------------------------------------------------------+
| ``viewkineticprofiles``    | Shows plasma kinetic profiles from the core                  |
|                            | profiles  (replaces kinplot).                                |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewkineticprofiles -p 134174 -r 117                    |
+----------------------------+--------------------------------------------------------------+
| ``viewmachinedescription`` | Plots machine description data stored in databases.          |
|                            | (replaces mdplot)                                            |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewmachinedescription plot wall pf_active              |
|                            |    $ viewmachinedescription list pf_active                   |
|                            |    $ viewmachinedescription plot wall                        |
+----------------------------+--------------------------------------------------------------+
| ``viewneutron``            | Plots particles vs normalised toroidal                       |
|                            | flux coordinate  (replaces neutronplot).                     |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewneutron -p 121014 -r 11 -t 450                      |
+----------------------------+--------------------------------------------------------------+
| ``viewplasmacompo``        | Display the plasma composition from the                      |
|                            | core_profiles IDS  (replaces ids_compo).                     |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewplasmacompo -p 131047 -r 4                          |
+----------------------------+--------------------------------------------------------------+
| ``viewpressure``           | Display the plasma kinetic profiles from .                   |
|                            | the core_profiles  (replaces pressureplot).                  |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewpressure -p 134174 -r 117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewrotation``           | Plasma kinetic profiles from the core_profiles               |
|                            | (replaces rotationplot)                                      |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewrotation -p 134174 -r 117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewscenario``           | Display the plasma kinetic profiles and equilibrium from     | 
|                            | the core_profiles and equilibrium  (replaces scenplot).      | 
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewscenario -p 134174 -r 117                           |
|                            |    $ viewscenario -p 134174 -r 117 --noProfiles              |
+----------------------------+--------------------------------------------------------------+
| ``viewsources``            | Shows source information from available                      |
|                            |  sources (replaces print_sources).                           |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewsources -p 134174 -r  117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewspectrometry``       | Displays the spectrum, displaying plots of radiance          |
|                            | and intensity in two different windows (replaces svplot).    |   
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewspectrometry -d TEST -p 134000 -r 37                |
+----------------------------+--------------------------------------------------------------+
| ``viewwall``               | Shows outline plot using limiter and vessel properties found | 
|                            | in 2D description of Wall IDS.                               | 
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewwall wall iter                                      |
+----------------------------+--------------------------------------------------------------+


************************
 IDS Manipulation Tools
************************

+---------------------+---------------------------------------------------------------------+
| Command             | Description and Example Usage                                       |
+=====================+=====================================================================+
| ``eqdsk2ids``       | EQDSK Convertor.                                                    | 
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ eqdsk2ids -p 134174 -r 117 -g resources/geqdsk/example.gfile   |
|                     |    -u $USERNAME -d ITER                                             |
+---------------------+---------------------------------------------------------------------+
| ``idschk``          | Validate ids fields against rules defined in yaml file              |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idschk -p 134174 -r 117 -f resources/validation_schemas/ITER   |
|                     |    /core_profiles.yml                                               |
+---------------------+---------------------------------------------------------------------+
| ``idscp``           | Copy ids from one pulse to another                                  |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idscp -pi 131024 -ri 10 -po 145000 -ro 2                       |
+---------------------+---------------------------------------------------------------------+
| ``idsdiff``         | Shows ids level differences between two runs. It stores result in   |
|                     | html document. For signals differences it is also shown as graph.   |  
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idsdiff --generate-html --pulseA 122525 --runA 1 122525 2      |
|                     |    --pulseB 122525 --runB 2 summary                                 |
+---------------------+---------------------------------------------------------------------+
| ``idslist``         | Shows list of all idses along with count of time slices.            |
|                     | (replaces ids_content(yaml), listidss (with time slices),           |    
|                     | idsoccurrences(occ) merged into one script)                         |                                            
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |  
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idslist -p 134174 -r 117                                       |
|                     |    $ idslist -p 134174 -r 117 yaml                                  |
|                     |    $ idslist -p 134174 -r 117 occ                                   |                                                                                                                                                                                                                                                                                
+---------------------+---------------------------------------------------------------------+
| ``idsperf``         | Shows performance of access layer operations on dataset. timing and |
|                     | performance information for different types of operations on IDS    |
|                     | data with the IMAS Python Access Layer.                             |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idsperf -p 134174 -r 117                                       |
|                     |    $ idsperf -p 134174 -r 117 equilibrium                           |
|                     |    $ idsperf -p 134174 -r 117 equilibrium --showStats --repeat 2    |
|                     |    $ idsperf -p 134174 -r 117 equilibrium  -a                       |
|                     |    $ idsperf -p 134174 -r 117 equilibrium -do HBD -bo MDSPLUS -o 412|
|                     |    $ idsperf -p 134174 -r 117 equilibrium  -t 50 -m                 |
+---------------------+---------------------------------------------------------------------+
| ``idsprint``        | Dumps or prints all data on the console.                            |
|                     | Check if specific fields or attributes have been filled out or empty|
|                     | The output can also be saved to a file using extraction             |
|                     | (Replaces idsdump, idsdumppath)                                     |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idsprint -p 134174 -r 117 equilibrium                          |
+---------------------+---------------------------------------------------------------------+
| ``idsresample``     | Resample IDSs from a data-entry and save them into another          |
|                     | data-entry based on PREVIOUS_INTERP method.                         |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |                                                                                                                                                                                                                                                                                                                                                
|                     |    $ idsresample -pi 131024 -ri 10 -po 145000 -ro 2 -u public       |                                                                                                                                                                                                                                 
+---------------------+---------------------------------------------------------------------+
| ``idsrescale``      | Rescaling an equilibrium magnetic field, storing the output into    |
| ``_equilibrium``    | another entry of the same DB. replaced by ids_rescale_eq            |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |                                                                                                                                                                                                                                                                                                                                                
|                     |    $ idsresample -pi 131024 -ri 10 -po 145000 -ro 2                 |                                                                                                                                                                                                                                 
+---------------------+---------------------------------------------------------------------+
| ``idsshift``        | Rigidly shifts vertically an equilibrium, storing the output into   |
| ``_equilibrium``    | another entry of the same DB. replaced by ids_shift_eq              |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |                                                                                                                                                                                                                                                                                                                                                
|                     |    $ idsshift_equilibrium -pi 122525 -ri 1 -po 123001 -ro 1         |                                                                                                                                                                                                                                 
|                     |    --shift -0.01                                                    |                                                                                                                                                                                                                                 
+---------------------+---------------------------------------------------------------------+
| ``idssize``         | IDS size in bytes and the time taken to read each object. It also   |
|                     | shows total size of all IDS objects in the data entry. It shows     |
|                     | total time taken to read all objects from the data entry. It is     |
|                     | helpful for performance check of IDS objects.                       |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idssize -p 122525 -r 1                                         |
+---------------------+---------------------------------------------------------------------+


****************
 Database Tools
****************

+---------------------+---------------------------------------------------------------------+
| Command             | Description and Example Usage                                       |
+=====================+=====================================================================+
| ``dbconverter``     | Copy all data-entries from one database into another one            |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |   $ dbconverter --user <username> --database ITER -do MYDB -bo HDF5 |
+---------------------+---------------------------------------------------------------------+
| ``dblist``          | Lists existing IMAS databases (Replaces imasdbs).                   |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ dblist -u public -d TEST list                                  |
|                     |    $ dblist -u public -d TEST list -c                               |
|                     |    $ dblist -u public -d TEST list -M                               |
|                     |    $ dblist databases                                               |
|                     |    $ dblist dataversions                                            |
+---------------------+---------------------------------------------------------------------+
| ``dbperf``          | Check performance of database                                       |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |   $ dbperf -d TEST                                                  |
+---------------------+---------------------------------------------------------------------+
| ``dbscraper``       | The `dbscraper` script scrapes data from a particular               |
|                     | IDS path for a specified series of pulses and displays the pulse    |
|                     | along with the value.  (Replaces db_extractor)                      |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ dbscraper "equilibrium/time_slice*0*/global_quantities/volume" |
|                     |    --list-count 2                                                   |
|                     |    dbscraper \"core_profiles/profiles_1d(0)/electrons/temperature\" |
|                     |    --list-count 2                                                   |
+---------------------+---------------------------------------------------------------------+
| ``dbselector``      | The `dbselector` script shows lists of all scenarios where          |
|                     | specified ids exists. Just provide idsname as input argument to the |
|                     | script.                                                             |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ dbselector -d TEST core_profiles --list-count 2                |
|                     |    $ dbselector -d TEST summary --list-count 2                      |
+---------------------+---------------------------------------------------------------------+

*************************
 Scenario Database Tools
*************************

+--------------------------------+---------------------------------------------------------------------+
| Command                        | Description and Example Usage                                       |
+================================+=====================================================================+
| ``create_db_entry``            | Auto-generated yaml scenario and watcher files                      |
+--------------------------------+---------------------------------------------------------------------+
| ``create_db_entry_disruption`` | Auto-generated yaml scenario and watcher files for disruption       |
|                                | database                                                            |
+--------------------------------+---------------------------------------------------------------------+
| ``create_validation_schema``   | Create validation schema using data dictionary validation attributes|
+--------------------------------+---------------------------------------------------------------------+
| ``disruption_summary``         | Script to list available disruptions in a specific folder           |
+--------------------------------+---------------------------------------------------------------------+
| ``md_status``                  | Show status and potential parent and children for a given           |
|                                | simulation stored in ITER machine description database folder       |
+--------------------------------+---------------------------------------------------------------------+
| ``md_summary``                 | md_summary list available machine description data in a specific    |
|                                | folder with search facility                                         |
+--------------------------------+---------------------------------------------------------------------+
| ``scenario_status``            | The `scenario_status` program provides information about the        |
|                                | scenario of specified shot and run number from the scenario         |
|                                | database. It shows status and potential parent and children for a   |
|                                | given simulation stored in ITER scenario description database       |
|                                | folder                                                              |
|                                |                                                                     |
|                                | .. code-block:: bash                                                |
|                                |                                                                     |
|                                |    $ scenario_status -p 134174 -r 117                               |
|                                |    $ scenario_status -p 130012 -r 4 --print                         |
+--------------------------------+---------------------------------------------------------------------+
| ``scenario_summary``           | The `scenario_summary` lists available scenarios in a specific      |
|                                | folder with search facility.                                        |
|                                |                                                                     |
|                                | .. code-block:: bash                                                |
|                                |                                                                     |
|                                |    $ scenario_summary -p He4,2.65                                   |
|                                |    $ scenario_summary -p He4,2.65 -c shot,run,database,composition  |
|                                |    $ scenario_summary -p He4 2.65                                   |
+--------------------------------+---------------------------------------------------------------------+
| ``show_db_entry``              | Show full description file for a given simulation stored in ITER DB |
|                                | folder.                                                             |
|                                |                                                                     |
|                                | .. code-block:: bash                                                |
|                                |                                                                     |
|                                |    $ show_db_entry -p 134174 -r 117                                 |
+--------------------------------+---------------------------------------------------------------------+
| ``validate_db_entry``          | Validation Tool for ITER Scenario DB                                |
+--------------------------------+---------------------------------------------------------------------+
| ``watch_db_entry``             | Subscribe/unsubscribe as a watcher to a simulation file             |
|                                | stored in IMAS DB                                                   |
+--------------------------------+---------------------------------------------------------------------+

