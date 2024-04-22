###################
 validate_db_entry
###################

Validation Tool for ITER Scenario DB

**************************
 Syntax validate_db_entry
**************************

   .. command-output:: validate_db_entry -h


***********************
 Example show_db_entry
***********************

.. code-block:: bash

      $ validate_db_entry -p 134174 -r 117 --path resources/validation_schemas
      24/04/22 22:50:46 INFO: -----------------------------------------------------------
      24/04/22 22:50:46 INFO: START: scripts/validate_db_entry
      24/04/22 22:50:46 INFO: -----------------------------------------------------------
      24/04/22 22:50:46 INFO: loading schema...
      24/04/22 22:50:47 INFO: -----------------------------------------------------------
      24/04/22 22:50:47 INFO: 1/1 (100%) 134174/117
      24/04/22 22:50:47 INFO: -----------------------------------------------------------
      24/04/22 22:50:47 INFO: - 134174/117/core_profiles/0 < schema
      24/04/22 22:50:50 ERROR:
      core_profiles:
         occurence(0):
            profiles_1d[0].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[1].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[2].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[3].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[4].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[5].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[6].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[7].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[8].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[9].grid.rho_tor_norm[:]:
            - Must be larger than 0.0
            profiles_1d[10].grid.rho_tor_norm[:]:




