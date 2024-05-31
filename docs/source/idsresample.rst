#############
 idsresample
#############

*idsresample* Resample IDSs from a data-entry and save them into another
data-entry based on `PREVIOUS_INTERP` method.. more about
`imas.imasdef.PREVIOUS_INTERP`: Interpolation method that returns the
previous time slice if the requested time does not exactly exist in the
original IDS

********************
 Syntax idsresample
********************

   .. command-output:: idsresample -h


*********************
 Example idsresample
*********************

    .. code-block:: bash

        $ idsresample --src "imas:mdsplus?user=public;pulse=131024;run=10;database=ITER;version=3" --dest "imas:mdsplus?user=username;pulse=131024;run=2;database=ITER;version=3"
