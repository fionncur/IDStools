idsshift_equilibrium
======================

*idsshift_equilibrium*  This script imports an equilibrium IDS, rigidly shifts it vertically, and then adds it to the output IDS


Syntax idsshift_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. command-output:: idsshift_equilibrium -h


Example idsshift_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsshift_equilibrium --src "imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3" --dest "imas:mdsplus?user=$USER;pulse=123001;run=1;database=ITER;version=3"  --shift -0.01
        [10/30/24 15:56:24] INFO     Shifting equilibrium by -0.01 m                                                               idsshift_equilibrium:69
                            INFO     Values for wall gaps, locations of strike-points and closest wall points are no longer        idsshift_equilibrium:70
                                    guaranteed!                                                                                                          
                            INFO     Equilibrium IDS is upward shifted successfully.                                               idsshift_equilibrium:80
                            INFO     Output database details                                                                       idsshift_equilibrium:83
                                    imas:mdsplus?user=username;pulse=123001;run=1;database=ITER;version=3                                                                   