###########
 eqdsk2ids
###########

*eqdsk2ids* EQDSK Convertor

******************
 Syntax eqdsk2ids
******************

   .. command-output:: eqdsk2ids -h

Example eqdsk2ids
~~~~~~~~~~~~~~~~~

   .. code-block:: bash

        $ eqdsk2ids -c 11 -g resources/geqdsk/example.gfile --dest \"imas:hdf5?user=$USERNAME;pulse=134174;run=117;database=ITER;version=3?path=$DATABASE_DIR\" --log INFO"
