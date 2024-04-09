idsrescale_equilibrium
======================

*idsrescale_equilibrium*  This script imports an equilibrium IDS, rescales its magnetic field components,
and then stores it to the output IDS


Syntax idsrescale_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash     

        $ idsrescale_equilibrium -h
        usage: idsrescale_equilibrium [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -si SHOT_INPUT -ri RUN_INPUT -so SHOT_OUTPUT -ro
                                    RUN_OUTPUT [-do DATABASE_OUTPUT] [-bo BACKEND_OUTPUT] --rescale RESCALE

        Rescaling an equilibrium magnetic field, storing the output into another entry of the same DB. replaced by ids_rescale_eq

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
        --rescale RESCALE     Rescaling factor of the equilibrium magnetic field


Example idsrescale_equilibrium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsrescale_equilibrium -si 134174 -ri 117 -so 122222 -ro 22 --rescale 2
        [04/08/24 10:37:27] INFO     Rescaling equilibrium magnetic field by 5.0                                                                idsrescale_equilibrium.py:100
        [04/08/24 10:37:33] INFO     Equilibrium IDS is rescaled successfully. database:ITER, shot:122222, run=22, user:sawantp1                idsrescale_equilibrium.py:111
                            INFO     Output database details database=ITER, shot=122222, run=22, user=sawantp1                                  idsrescale_equilibrium.py:114



