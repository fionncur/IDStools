idsshift_equilibrium
======================

*idsshift_equilibrium*  This script imports an equilibrium IDS, rigidly shifts it vertically, and then adds it to the output IDS


Syntax idsshift_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash     

        $ idsshift_equilibrium -h
        Usage: idsshift_equilibrium [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -si SHOT_INPUT -ri RUN_INPUT -so SHOT_OUTPUT -ro
                            RUN_OUTPUT [-do DATABASE_OUTPUT] [-bo BACKEND_OUTPUT] --shift SHIFT

        Rigidly shifts vertically an equilibrium, storing the output into another entry of the same DB

        Optional Arguments:
        -h, --help            show this help message and exit
        -u, --user_or_path USER
                                user (default=public)
        --database, -d DATABASE
                                database name (default=ITER)
        --backend, -b BACKEND
                                backend format (default=MDSPLUS)
        --version, -v VERSION
                                data version (default=3)
        -si, --shot_input SHOT_INPUT
                                Input shot number
        -ri, --run_input RUN_INPUT
                                Input run number
        -so, --shot_output SHOT_OUTPUT
                                Output shot number
        -ro, --run_output RUN_OUTPUT
                                Output run number
        -do, --database_output DATABASE_OUTPUT
                                Database name for the destination data-entry
        -bo, --backend_output BACKEND_OUTPUT
                                Backend name for the destination data-entry
        --shift SHIFT         Upward shift of equilibrium (m)

Example idsshift_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsshift_equilibrium -si 134174 -ri 117 -so 123001 -ro 1 --shift -0.01
        [04/08/24 11:33:06] INFO     Shifting equilibrium by -0.01 m                                                                                  idsshift_equilibrium:95
                            INFO     Values for wall gaps, locations of strike-points and closest wall points are no longer guaranteed!               idsshift_equilibrium:96
        [04/08/24 11:33:08] INFO     Equilibrium IDS is upward shifted successfully.                                                                 idsshift_equilibrium:108
                            INFO     Output database details database=ITER, shot=123001, run=1, user=sawantp1                                        idsshift_equilibrium:109