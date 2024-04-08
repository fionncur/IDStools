idsrescale_equilibrium
======================

*idsrescale_equilibrium*  This script imports an equilibrium IDS, rescales its magnetic field components,
and then stores it to the output IDS


Syntax idsrescale_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash     

        $ idsrescale_equilibrium -h
        usage: idsrescale_equilibrium [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -si SHOT_INPUT -ri RUN_INPUT -so SHOT_OUTPUT -ro
                                    RUN_OUTPUT [-do DATABASE_OUTPUT] [-bo BACKEND_OUTPUT] -r RESCALEFACTOR

        Rescaling an equilibrium magnetic field, storing the output into another entry of the same DB

        optional arguments:
        -h, --help            show this help message and exit
        -u USER, --user_or_path USER
                                user (default=public)
        --database DATABASE, -d DATABASE
                                database name (default=ITER)
        --backend BACKEND, -b BACKEND
                                backend format (default=MDSPLUS)
        --version VERSION, -v VERSION
                                data version (default=3)
        -si SHOT_INPUT, --shot_input SHOT_INPUT
                                Input shot number
        -ri RUN_INPUT, --run_input RUN_INPUT
                                Input run number
        -so SHOT_OUTPUT, --shot_output SHOT_OUTPUT
                                Output shot number
        -ro RUN_OUTPUT, --run_output RUN_OUTPUT
                                Output run number
        -do DATABASE_OUTPUT, --database_output DATABASE_OUTPUT
                                Database name for the destination data-entry
        -bo BACKEND_OUTPUT, --backend_output BACKEND_OUTPUT
                                Backend name for the destination data-entry
        -r RESCALEFACTOR, --rescaleFactor RESCALEFACTOR
                                Rescaling factor of the equilibrium magnetic field


Example idsrescale_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsrescale_equilibrium -si 134174 -ri 117 -r 5 -so 122222 -ro 22
        [04/08/24 10:37:27] INFO     Rescaling equilibrium magnetic field by 5.0                                                                idsrescale_equilibrium.py:100
        [04/08/24 10:37:33] INFO     Equilibrium IDS is rescaled successfully. database:ITER, shot:122222, run=22, user:sawantp1                idsrescale_equilibrium.py:111
                            INFO     Output database details database=ITER, shot=122222, run=22, user=sawantp1                                  idsrescale_equilibrium.py:114



