########
 idschk
########

*idschk* validate ids fields against rules defined in yaml file.

***************
 Syntax idschk
***************

   .. code-block:: bash

      $ idschk -h
      Install tqdm to enable progress bar
      usage: idschk [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-l [IDSLIST [IDSLIST ...]]] [-t [TIME]] [-f SCHEMA_FILE] [--ipsign {-1,1}]
                  [--b0sign {-1,1}] [--verbose] [-c]

      Load IMAS and install Cerberus (if not done before)
          $ module load IMAS
          $ pip install cerberus

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
      -s SHOT, --shot SHOT  Shot number
      -r RUN, --run RUN     Run number
      -l [IDSLIST [IDSLIST ...]], --list [IDSLIST [IDSLIST ...]]
                              IDS names to be checked
      -t [TIME], --time [TIME]
                              time (default=middle)
      -f SCHEMA_FILE, --schema_file SCHEMA_FILE
                              file name of validation schema
      --ipsign {-1,1}       sign(Ip), default=-1
      --b0sign {-1,1}       sign(B0), default=-1
      --verbose             increase output verbosity
      -c, --cocos           compute COCOS values from IDS/equilibrium

****************
 Example idschk
****************

   .. code-block:: bash

      $ idschk -s 134174 -r 117 -f /home/ITER/sawantp1/git/idstools/database_tools/validation_schemas/generic/core_profiles.yml

      Install tqdm to enable progress bar
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

      # Command Line Interface for IDS Data Validation (idschk)
      # Examples:
      #Validate if ITER Scenario meets with physics requirements
      $ idschk -s 131024 -r 40 -f path/to/schema_file/required_fields_core.yml

      #Same with 1) and only for one time slice. Specify time, otherwise middle point if blank
      $ idschk -s 131024 -r 40 -f path/to/schema_file/required_fields_core.yml -t 100.
      $ idschk -s 131024 -r 40 -f path/to/schema_file/required_fields_core.yml -t

      #Check IDS/equilibrium for COCOS
      $ idschk -s 131024 -r 40 -c

      # Check IDS/equilibrium with COCOS values
      $ idschk -s 131024 -r 40 -c --verbose

   .. code-block:: python

      # Functional Interface in Python (database_tools/idschk.py)
      # Examples:
      # 0) Initialization
      import imas
      from database_tools.idschk import *

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
