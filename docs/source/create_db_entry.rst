#################
 create_db_entry
#################

Auto-generated yaml scenario and watcher files

************************
 Syntax create_db_entry
************************

    .. command-output:: create_db_entry -h

*************************
 Example create_db_entry
*************************

    .. code-block:: bash

        $ create_db_entry -p 130012 -r 105 -d TEST
        ----> summary IDS did not include power_loss
        P_sol will be deduced from edge_transport if available
        --------------------------------------------------------
        The summary IDS is absent from the input data-entry
        ----> H&CD waveforms not filled: to be completed by hand
        --------------------------------------------------------
        core_profiles:
            occurence(0):
                profiles_1d[2].ion[1].pressure_fast_perpendicular[:]:
                - Must be larger than 0.0
                profiles_1d[3].ion[1].pressure_fast_perpendicular[:]:
                - Must be larger than 0.0
                profiles_1d[4].ion[1].pressure_fast_perpendicular[:]:
                - Must be larger than 0.0
                profiles_1d[5].ion[1].pressure_fast_perpendicular[:]:
                - Must be larger than 0.0
                profiles_1d[2].ion[1].pressure_fast_parallel[:]:
                - Must be larger than 0.0
                profiles_1d[3].ion[1].pressure_fast_parallel[:]:
                - Must be larger than 0.0
                profiles_1d[4].ion[1].pressure_fast_parallel[:]:
                - Must be larger than 0.0
                profiles_1d[5].ion[1].pressure_fast_parallel[:]:
                - Must be larger than 0.0

        equilibrium:
            occurence(0): {}

        24/04/22 14:14:25 ERROR: IDS validation failed. Use '--disable-validation' for generating yaml and watcher files anyway


    .. code-block:: bash

        $ create_db_entry -p 130012 -r 105 -d TEST --disable-validation
        ----> summary IDS did not include power_loss
        P_sol will be deduced from edge_transport if available
        --------------------------------------------------------
        The summary IDS is absent from the input data-entry
        ----> H&CD waveforms not filled: to be completed by hand
        --------------------------------------------------------
        ----> ids_1300120105.yaml created.
        ----> ids_1300120105.watcher created.