###################
 viewcoretransport
###################

*viewcoretransport* Displays the Core plasma transport of particles,
energy, momentum and poloidal flux.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

**************************
 Syntax viewcoretransport
**************************

   .. command-output:: viewcoretransport -h

***************************
 Example viewcoretransport
***************************

   .. code-block:: bash

        $ viewcoretransport -p 92436 -r 850 -d TEST 
        $ viewcoretransport --uri "imas:mdsplus?user=public;shot=92436;run=850;database=TEST;version=3" 

   .. thumbnail:: _static/images/viewcoretransport.png
      :alt: image not found
      :align: center
