#######
 idscp
#######

*idscp* tool helps you to copy ids from one pulse to another

**************
 Syntax idscp
**************

   .. program-output:: idscp -h

***************
 Example idscp
***************

   .. code-block:: bash

      $ idscp -sp 131024 -sr 10 -dp 145000 -dr 32 -u public 
      Copying equilibrium

   .. code-block:: bash

      $ idscp --src "imas:mdsplus?user=public;shot=131024;run=10;database=ITER;version=3" --dest "imas:mdsplus?user=username;shot=145000;run=5;database=ITER;version=3"