#####################
 IDStools Cheatsheet
#####################

This cheat sheet provides quick references for commonly used commands in
IDStools. :download:`download cheatsheet here <_static/cheatsheet.pdf>`

***********
 IDS Tools
***********

+---------------------+---------------------------------------------------------------------+
| Command             | Description and Example Usage                                       |
+=====================+=====================================================================+
| ``idschk``          | Validate ids fields against rules defined in yaml file              |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ idschk -s 134174 -r 117 -f core_profiles.yml                   |
+---------------------+---------------------------------------------------------------------+
| ``idscp``           | Copy ids from one pulse to another                                  |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ idscp -si 131024 -ri 10 -so 145000 -ro 2                       |
+---------------------+---------------------------------------------------------------------+
| ``idsdiff``         | Shows ids level differences between two runs. It stores result in   |
|                     | html document. For signals differences it is also shown as graph.   |  
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ idsdiff --generate-html 122525 1 122525 2 summary              |
+---------------------+---------------------------------------------------------------------+
| ``idslist``         | Shows list of all idses along with count of time slices.            |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |  
|                     | .. code:: bash                                                      |
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
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ idsperf -s 134174 -r 117                                       |
|                     |    $ idsperf -s 134174 -r 117 equilibrium                           |
|                     |    $ idsperf -s 134174 -r 117 equilibrium --showStats --repeat 2    |
|                     |    $ idsperf -s 134174 -r 117 equilibrium  -a                       |
|                     |    $ idsperf -s 134174 -r 117 equilibrium -do HBD -bo MDSPLUS -o 412|
|                     |    $ idsperf -s 134174 -r 117 equilibrium  -t 50 -m                 |
+---------------------+---------------------------------------------------------------------+
| ``idsprint``        | Dumps or prints all data on the console. Check if specific fields   |
|                     | or attributes have been filled out or empty . The output can also   |
|                     | be saved to a file using extraction                                 |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ idsprint -s 134174 -r 117 equilibrium                          |
+---------------------+---------------------------------------------------------------------+
| ``idsresample``     | Resample IDSs from a data-entry and save them into another          |
|                     | data-entry based on PREVIOUS_INTERP method.                         |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |                                                                                                                                                                                                                                                                                                                                                
|                     |    $ idsresample -si 131024 -ri 10 -so 145000 -ro 2                 |                                                                                                                                                                                                                                 
+---------------------+---------------------------------------------------------------------+
| ``idssize``         | IDS size in bytes and the time taken to read each object. It also   |
|                     | shows total size of all IDS objects in the data entry. It shows     |
|                     | total time taken to read all objects from the data entry. It is     |
|                     | helpful for performance check of IDS objects.                       |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ idssize -s 122525 -r 1                                         |
+---------------------+---------------------------------------------------------------------+
| ``eqdsk2ids``       | EQDSK Convertor.                                                    |                                                                                                                                                                                                                                                                                                                                
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ eqdsk2ids -s 134174 -r 117 -g example.gfile -u <user> -d ITER  |
|                     |    --log INFO                                                       |
+---------------------+---------------------------------------------------------------------+


****************
 Analysis Tools
****************

+----------------------------+--------------------------------------------------------------+
| Command                    | Description                                                  |
+============================+==============================================================+
|``viewcoresources``         | Plots core_sources results.                                  |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewcoresources -s 130012 -r 5 -u username -d ITER      |
+----------------------------+--------------------------------------------------------------+
|``viewecstrayradiation``    | Shows electron cyclotron stray radiation.                    |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewecstrayradiation -s 134174 -r 117                   |
+----------------------------+--------------------------------------------------------------+
| ``viewedgeprofiles``       | Shows edge profiles plots by interpolating on rectangular    |
|                            | grid.                                                        |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewedgeprofiles -s 123314 -r 1                         |
+----------------------------+--------------------------------------------------------------+
| ``viewequilibrium``        | Shows plasma equilibrium.                                    |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewequilibrium -s 134174 -r 117 --rho --pfcoils --info |
+----------------------------+--------------------------------------------------------------+
| ``viewfluxes``             | Shows flux information from available transport models.      |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewfluxes -s 134174 -r  117 -m CLOSEST                 |
+----------------------------+--------------------------------------------------------------+
| ``viewkineticprofiles``    | Shows plasma kinetic profiles from the core profiles.        |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewkineticprofiles -s 134174 -r 117                    |
+----------------------------+--------------------------------------------------------------+
| ``viewmachinedescription`` | Plots machine description data stored in databases.          |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewmachinedescription -d ITER_MD                       |
+----------------------------+--------------------------------------------------------------+
| ``viewneutron``            | Plots particles vs normalised toroidal flux coordinate.      |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewneutron -s 121014 -r 11 -t 450 --info               |
+----------------------------+--------------------------------------------------------------+
| ``viewpressure``           | Display the plasma kinetic profiles from the core_profiles.  |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewpressure -s 134174 -r 117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewscenario``           | Display the plasma kinetic profiles and equilibrium from .   |   
|                            | the core_profiles and equilibrium                            |                                                                         
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewscenario -s 134174 -r 117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewrotation``           | Plasma kinetic profiles from the core_profiles.              |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewrotation -s 134174 -r 117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewsources``            | Shows source information from available sources.             |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewsources -s 134174 -r  117                           |
+----------------------------+--------------------------------------------------------------+
| ``viewspectrometry``       | Displays the spectrum, displaying plots of radiance and      |
|                            | intensity in two different windows.                          |   
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewspectrometry -u schneim -d 55.EC -s 134000 -r 37    |
|                            |    $ viewspectrometry --shot 150512 --run 3 --database       |
|                            |      ITER_MD                                                 |
+----------------------------+--------------------------------------------------------------+
| ``viewcoretransport``      | Core plasma transport of particles, energy, momentum and     |
|                            | poloidal flux.                                               |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewcoretransport -u costerd -d jet_reference_g2tjohns  |
|                            |     -s 92436 -r 850                                          |
+----------------------------+--------------------------------------------------------------+
| ``viewwall``               | Shows outline plot using limiter and vessel properties found | 
|                            | in 2D description of Wall IDS.                               | 
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewwall wall iter                                      |
+----------------------------+--------------------------------------------------------------+
| ``viewhcddistributions``   | Shows plot of distributions                                  |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewhcddistributions -s 130012 -r 5 -u username -d ITER |
+----------------------------+--------------------------------------------------------------+
| ``viewhcdplots``           | Shows plots from distributions and waves for different data  |
|                            | entries for analysis.                                        |
+----------------------------+--------------------------------------------------------------+
|                            |                                                              |
|                            | .. code:: bash                                               |
|                            |                                                              |
|                            |    $ viewhcdplots -s 130012 -r 5 -u username -d ITER         |
+----------------------------+--------------------------------------------------------------+

****************
 Database Tools
****************

+---------------------+---------------------------------------------------------------------+
| Command             | Description                                                         |
+=====================+=====================================================================+
| ``dblist``          | Lists existing IMAS databases.                                      |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ dblist databases                                               |
+---------------------+---------------------------------------------------------------------+
| ``dbscraper``       | The `dbscraper` script scrapes data from a particular IDS path for  |
|                     | a specified series of pulses and displays the pulse along with the  |
|                     | value.                                                              |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ dbscraper "equilibrium/time_slice(0)/global_quantities/volume" |
|                     |    --list-count 10                                                  |
+---------------------+---------------------------------------------------------------------+
| ``dbselector``      | The `dbselector` script shows lists of all scenarios where          |
|                     | specified ids exists. Just provide idsname as input argument to the |
|                     | script.                                                             |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ dbselector edge_profiles                                       |
+---------------------+---------------------------------------------------------------------+
| ``scenario_status`` | The `scenario_status` program provides information about the        |
|                     | scenario of specified shot and run number from the scenario         |
|                     | database. It shows status and potential parent and children for a   |
|                     | given simulation stored in ITER scenario description database       |
|                     | folder                                                              |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ scenario_status -s 134174 -r 117                               |
|                     |    $ scenario_status -s 130012 -r 4 --print                         |
+---------------------+---------------------------------------------------------------------+
| ``scenario_summary``| The `scenario_summary` lists available scenarios in a specific      |
|                     | folder with search facility.                                        |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ scenario_summary -s He4,2.65                                   |
|                     |    $ scenario_summary -s He4,2.65 -c shot,run,database,composition  |
|                     |    $ scenario_summary -s He4 2.65                                   |
+---------------------+---------------------------------------------------------------------+
| ``show_db_entry``   | Show full description file for a given simulation stored in ITER DB |
|                     | folder.                                                             |
+---------------------+---------------------------------------------------------------------+
|                     |                                                                     |
|                     | .. code:: bash                                                      |
|                     |                                                                     |
|                     |    $ show_db_entry -s 134174 -r 117                                 |
+---------------------+---------------------------------------------------------------------+
