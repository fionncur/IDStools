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

        $ idsrescale_equilibrium --src "imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3" --dest "imas:mdsplus?user=$USER;pulse=122222;run=22;database=ITER;version=3"  --rescale 2
        [10/30/24 15:54:16] INFO     Rescaling equilibrium magnetic field by 2.0                                                 idsrescale_equilibrium:77
        [10/30/24 15:54:17] INFO     Equilibrium IDS is rescaled successfully.                                                   idsrescale_equilibrium:88
                            INFO     Output database details                                                                     idsrescale_equilibrium:90
                                     imas:mdsplus?user=sawantp1;pulse=122222;run=22;database=ITER;version=3  


