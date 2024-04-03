#####################
 IDStools Cheatsheet
#####################

This cheat sheet provides quick references for commonly used commands in
IDStools. :download:`download cheatsheet here <_static/cheatsheet.pdf>`


****************
 Analysis Tools
****************

+----------------------------+--------------------------------------------------------------+
| Command                    | Description                                                  |
+============================+==============================================================+
|``viewcoresources``         | csplot Plots core_sources results.                           |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewcoresources -s 130012 -r 5 -u username -d ITER      |
+----------------------------+--------------------------------------------------------------+
| ``viewcoretransport``      | check_transport Core plasma transport of particles, energy,  |
|                            | momentum and poloidal flux.                                  |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewcoretransport -u public -d TEST -s 92436 -r 850     |
|                            |                                                              |
+----------------------------+--------------------------------------------------------------+
|``vieweccomposition``       | *eccomp* Display ec results.                                 |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ vieweccomposition -d TEST -s 134173 -r 2326             |
+----------------------------+--------------------------------------------------------------+
|``viewecray``               | *ecray* Display EC wave ray-tracing results.                 |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewecray -d TEST -s 134173 -r 2326                     |
+----------------------------+--------------------------------------------------------------+
|``viewecstrayradiation``    | Shows electron cyclotron stray radiation.                    |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewecstrayradiation -s 134174 -r 117                   |
+----------------------------+--------------------------------------------------------------+
| ``viewedgeprofiles``       | Shows edge profiles plots by interpolating on rectangular    |
|                            | grid.                                                        |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewedgeprofiles -s 123314 -r 1                         |
+----------------------------+--------------------------------------------------------------+
| ``viewequilibrium``        | *equiplot* Shows plasma equilibrium.                         |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewequilibrium -s 134174 -r 117 --rho --pfcoils --info |
+----------------------------+--------------------------------------------------------------+
| ``viewfluxes``             | *print_fluxes* Shows flux information from available         |
|                            | transport models.                                            |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewfluxes -s 134174 -r  117 -m CLOSEST                 |
+----------------------------+--------------------------------------------------------------+
| ``viewkineticprofiles``    | *kinplot* Shows plasma kinetic profiles from the core        |
|                            | profiles.                                                    |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewkineticprofiles -s 134174 -r 117                    |
+----------------------------+--------------------------------------------------------------+
| ``viewhcdplots``           | *hcd_plot* shows plots from distributions and waves for      |
|                            | different data entries for analysis                          |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ hcd_plot -ech 104104/2/schneim/MDSPLUS/TORBEAM_XMODE/3  |
|                            |    -nbi 130012/15/schneim/MDSPLUS/SPOT/3                     |
+----------------------------+--------------------------------------------------------------+
| ``viewhcdwaves``           | *hcd_waves_plot* shows waveforms                             |
|                            |                                                              |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $  viewhcdwaves -s 134173 -r 101 -u public -d TEST        |
+----------------------------+--------------------------------------------------------------+
| ``viewhcddistributions``   | *hcd_distributions_plot* shows waveforms                     |
|                            |                                                              |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewhcddistributions -s 130012 -r 115 -u public -d TEST |
+----------------------------+--------------------------------------------------------------+
| ``viewmachinedescription`` | *mdplot* Plots machine description data stored in databases. |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewmachinedescription -d ITER_MD                       |
+----------------------------+--------------------------------------------------------------+
| ``viewneutron``            | *neutronplot* Plots particles vs normalised toroidal         |
|                            | flux coordinate.                                             |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewneutron -s 121014 -r 11 -t 450 --info               |
+----------------------------+--------------------------------------------------------------+
| ``viewplasmacompo``        | *ids_compo* Display the plasma composition from the          |
|                            | core_profiles IDS                                            |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewplasmacompo -s 131047 -r 4                          |
+----------------------------+--------------------------------------------------------------+
| ``viewpressure``           | *pressureplot* Display the plasma kinetic profiles from .    |
|                            | the core_profiles                                            |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewpressure -s 134174 -r 117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewrotation``           | *rotationplot* Plasma kinetic profiles from the core_profiles|
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewrotation -s 134174 -r 117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewscenario``           | *scenplot* Display the plasma kinetic profiles and           | 
|                            | equilibrium from the core_profiles and equilibrium           | 
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewscenario -s 134174 -r 117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewsources``            | *print_sources* Shows source information from available      |
|                            |  sources.                                                    |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewsources -s 134174 -r  117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewspectrometry``       | *svplot* Displays the spectrum, displaying plots of radiance |
|                            | and intensity in two different windows.                      |   
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code-block:: bash                                         |
|                            |                                                              |
|                            |    $ viewspectrometry -d TEST -s 134000 -r 37                |
|                            |    $ viewspectrometry --shot 150512 --run 3 --database       |
|                            |      ITER_MD                                                 |
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
|                     |    $ eqdsk2ids -s 134174 -r 117 -g example.gfile -u <user> -d ITER  |
|                     |    --log INFO                                                       |
+---------------------+---------------------------------------------------------------------+
| ``idschk``          | Validate ids fields against rules defined in yaml file              |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idschk -s 134174 -r 117 -f core_profiles.yml                   |
+---------------------+---------------------------------------------------------------------+
| ``idscp``           | Copy ids from one pulse to another                                  |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idscp -si 131024 -ri 10 -so 145000 -ro 2                       |
+---------------------+---------------------------------------------------------------------+
| ``idsdiff``         | Shows ids level differences between two runs. It stores result in   |
|                     | html document. For signals differences it is also shown as graph.   |  
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idsdiff --generate-html 122525 1 122525 2 summary              |
+---------------------+---------------------------------------------------------------------+
| ``idslist``         | Shows list of all idses along with count of time slices.            |
|                     | [ids_content*yaml*, listidss *with time slices*, idsoccurrences*occ*|    
|                     | merged into one script]                                             |                                            
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |  
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idslist -s 134174 -r 117                                       |
|                     |    $ idslist -s 134174 -r 117 yaml                                  |
|                     |    $ idslist -s 134174 -r 117 occ                                   |                                                                                                                                                                                                                                                                                
+---------------------+---------------------------------------------------------------------+
| ``idsperf``         | Shows performance of access layer operations on dataset. timing and |
|                     | performance information for different types of operations on IDS    |
|                     | data with the IMAS Python Access Layer.                             |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idsperf -s 134174 -r 117                                       |
|                     |    $ idsperf -s 134174 -r 117 equilibrium                           |
|                     |    $ idsperf -s 134174 -r 117 equilibrium --showStats --repeat 2    |
|                     |    $ idsperf -s 134174 -r 117 equilibrium  -a                       |
|                     |    $ idsperf -s 134174 -r 117 equilibrium -do HBD -bo MDSPLUS -o 412|
|                     |    $ idsperf -s 134174 -r 117 equilibrium  -t 50 -m                 |
+---------------------+---------------------------------------------------------------------+
| ``idsprint``        | *idsdump, idsdumppath* Dumps or prints all data on the console.     |
|                     | Check if specific fields or attributes have been filled out or empty|
|                     | The output can also be saved to a file using extraction             |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idsprint -s 134174 -r 117 equilibrium                          |
+---------------------+---------------------------------------------------------------------+
| ``idsresample``     | Resample IDSs from a data-entry and save them into another          |
|                     | data-entry based on PREVIOUS_INTERP method.                         |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |                                                                                                                                                                                                                                                                                                                                                
|                     |    $ idsresample -si 131024 -ri 10 -so 145000 -ro 2                 |                                                                                                                                                                                                                                 
+---------------------+---------------------------------------------------------------------+
| ``idssize``         | IDS size in bytes and the time taken to read each object. It also   |
|                     | shows total size of all IDS objects in the data entry. It shows     |
|                     | total time taken to read all objects from the data entry. It is     |
|                     | helpful for performance check of IDS objects.                       |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ idssize -s 122525 -r 1                                         |
+---------------------+---------------------------------------------------------------------+


****************
 Database Tools
****************

+---------------------+---------------------------------------------------------------------+
| Command             | Description                                                         |
+=====================+=====================================================================+
| ``dblist``          | *imasdbs* Lists existing IMAS databases.                            |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ dblist databases                                               |
+---------------------+---------------------------------------------------------------------+
| ``dbscraper``       | *db_extractor* The `dbscraper` script scrapes data from a particular|
|                     | IDS path for a specified series of pulses and displays the pulse    |
|                     | along with the value.                                               |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ dbscraper "equilibrium/time_slice*0*/global_quantities/volume" |
|                     |    --list-count 10                                                  |
+---------------------+---------------------------------------------------------------------+
| ``dbselector``      | The `dbselector` script shows lists of all scenarios where          |
|                     | specified ids exists. Just provide idsname as input argument to the |
|                     | script.                                                             |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ dbselector edge_profiles                                       |
+---------------------+---------------------------------------------------------------------+

*************************
 Scenario Database Tools
*************************

+---------------------+---------------------------------------------------------------------+
| Command             | Description                                                         |
+=====================+=====================================================================+
| ``scenario_status`` | The `scenario_status` program provides information about the        |
|                     | scenario of specified shot and run number from the scenario         |
|                     | database. It shows status and potential parent and children for a   |
|                     | given simulation stored in ITER scenario description database       |
|                     | folder                                                              |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ scenario_status -s 134174 -r 117                               |
|                     |    $ scenario_status -s 130012 -r 4 --print                         |
+---------------------+---------------------------------------------------------------------+
| ``scenario_summary``| The `scenario_summary` lists available scenarios in a specific      |
|                     | folder with search facility.                                        |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ scenario_summary -s He4,2.65                                   |
|                     |    $ scenario_summary -s He4,2.65 -c shot,run,database,composition  |
|                     |    $ scenario_summary -s He4 2.65                                   |
+---------------------+---------------------------------------------------------------------+
| ``show_db_entry``   | Show full description file for a given simulation stored in ITER DB |
|                     | folder.                                                             |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code-block:: bash                                                |
|                     |                                                                     |
|                     |    $ show_db_entry -s 134174 -r 117                                 |
+---------------------+---------------------------------------------------------------------+
