idsshift_equilibrium
======================

*idsshift_equilibrium*  This script imports an equilibrium IDS, rigidly shifts it vertically, and then adds it to the output IDS


Syntax idsshift_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. command-output:: idsshift_equilibrium -h


Example idsshift_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsshift_equilibrium -sp 134174 -sr 117 -dp 123001 -dr 21 --shift -0.01
        $ idsshift_equilibrium --src "imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3" --dest "imas:mdsplus?user=usernameshot=123001;run=1;database=ITER;version=3"  --shift -0.01
        [04/08/24 11:33:06] INFO     Shifting equilibrium by -0.01 m                                                                                  idsshift_equilibrium:95
                            INFO     Values for wall gaps, locations of strike-points and closest wall points are no longer guaranteed!               idsshift_equilibrium:96
        [04/08/24 11:33:08] INFO     Equilibrium IDS is upward shifted successfully.                                                                 idsshift_equilibrium:108
                            INFO     Output database details database=ITER, shot=123001, run=1, user=sawantp1                                        idsshift_equilibrium:109