##########
 idsprint
##########

*idsprint* is a utility that, as the name implies, dumps or prints all
data on the console. It is handy if you need to rapidly verify if
specific fields or attributes have been filled out or empty . The output
can also be saved to a file using extraction.

*****************
 Syntax idsprint
*****************

   .. command-output:: idsprint -h


******************
 Example idsprint
******************

   .. code-block:: bash

      $ idsprint --uri "imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3" equilibrium

      class equilibrium
      Attribute ids_properties
          class ids_properties
          Attribute comment:
          Attribute homogeneous_time: 1
          Attribute source:
          Attribute provider:
          Attribute creation_date:
          Attribute version_put
