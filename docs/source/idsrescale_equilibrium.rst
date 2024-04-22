idsrescale_equilibrium
======================

*idsrescale_equilibrium*  This script imports an equilibrium IDS, rescales its magnetic field components,
and then stores it to the output IDS


Syntax idsrescale_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. command-output:: idsrescale_equilibrium -h


Example idsrescale_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsrescale_equilibrium -sp 134174 -sr 117 -dp 122222 -dr 22 --rescale 2
        $ idsrescale_equilibrium --src "imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3" --dest "imas:mdsplus?user=sawantp1;shot=122222;run=22;database=ITER;version=3"  --rescale 2
        [04/08/24 10:37:27] INFO     Rescaling equilibrium magnetic field by 5.0                                                                idsrescale_equilibrium.py:100
        [04/08/24 10:37:33] INFO     Equilibrium IDS is rescaled successfully. database:ITER, shot:122222, run=22, user:sawantp1                idsrescale_equilibrium.py:111
                            INFO     Output database details database=ITER, shot=122222, run=22, user=sawantp1                                  idsrescale_equilibrium.py:114



