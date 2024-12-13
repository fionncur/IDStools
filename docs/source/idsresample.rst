#############
 idsresample
#############

*idsresample* Resample IDSs from a data-entry and save them into another
data-entry based on `PREVIOUS_INTERP` method.. more about
`imas.ids_defs.PREVIOUS_INTERP`: Interpolation method that returns the
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

        $ idsresample --src "imas:mdsplus?user=public;shot=131024;run=10;database=ITER;version=3" --dest "imas:mdsplus?user=$USER;shot=131024;run=5;database=ITER;version=3" --index-range 0,,10
        resampling indices :core_profiles
        resampling indices :distribution_sources
        resampling indices :equilibrium
        resampling indices :pf_active
        resampling indices :summary

