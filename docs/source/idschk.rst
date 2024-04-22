########
 idschk
########

*idschk* validate ids fields against rules defined in yaml file.

***************
 Syntax idschk
***************

   .. command-output:: idschk -h


****************
 Example idschk
****************

   .. code-block:: bash

      $ idschk -p 134174 -r 117 -f resources/validation_schemas/ITER/core_profiles.yml

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

   .. code-block:: bash

      idschk --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" -f resources/validation_schemas/generic/core_profiles.yml

   .. code-block:: bash

      # Command Line Interface for IDS Data Validation (idschk)
      # Examples:
      #Validate if ITER Scenario meets with physics requirements
      $ idschk -p 131024 -r 40 -f path/to/schema_file/required_fields_core.yml

      #Same with 1) and only for one time slice. Specify time, otherwise middle point if blank
      $ idschk -p 131024 -r 40 -f path/to/schema_file/required_fields_core.yml -t 100.
      $ idschk -p 131024 -r 40 -f path/to/schema_file/required_fields_core.yml -t

      #Check IDS/equilibrium for COCOS
      $ idschk -p 131024 -r 40 -c

      # Check IDS/equilibrium with COCOS values
      $ idschk -p 131024 -r 40 -c --verbose

   .. code-block:: python

      # Functional Interface in Python (idstools/idschk.py)
      # Examples:
      # 0) Initialization
      import imas
      from idstools.idschk import *

      input = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND, "ITER", 131024, 40, "public")
      input.open()
      equilibrium = input.get("equilibrium")

      # 1) Validate if ITER Scenario meets with physics requirements
      flag, log = ids_validator(equilibrium, "path/to/schema_file/required_fields_core.yml")

      # 2) Validate length of coordinate for INT_*D and FLT_*D
      flag, log = ids_coordinate_check(equilibrium)

      # 3) Same with 2), increasing verbosity,
      flag, log = ids_coordinate_check(equilibrium, verbose=True)

      # 4) Compute COCOS
      cocos = ids_compute_cocos(equilibrium)

      # 5) Get COCOS values
      flag, log = ids_cocos_check(equilibrium, verbose=True)
