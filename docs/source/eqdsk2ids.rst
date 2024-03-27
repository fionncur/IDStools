###########
 eqdsk2ids
###########

*eqdsk2ids* EQDSK Convertor

******************
 Syntax eqdsk2ids
******************

   .. code-block:: bash

      $ eqdsk2ids -h
      usage: eqdsk2ids [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN -g GPATH [--log {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--ipsign {-1,0,1}]
               [--b0sign {-1,0,1}] [--cocos_in {1,2,3,4,5,6,7,8,11,12,13,14,15,16,17,18}]

       optional arguments:
      -h, --help            show this help message and exit
      -u USER, --user_or_path USER
                              user (default=sawantp1)
      --database DATABASE, -d DATABASE
                              database name (default=ITER)
      --backend BACKEND, -b BACKEND
                              backend format (default=MDSPLUS)
      --version VERSION, -v VERSION
                              data version (default=3)
      -s SHOT, --shot SHOT  Shot number
      -r RUN, --run RUN     Run number
      -g GPATH, --gfile GPATH
                              path to GEQDSK file
      --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                              Configure the logging level, default=WARNING
      --ipsign {-1,0,1}     transform input data to obtain desired sign for Ip on the output, default=0 uses input
      --b0sign {-1,0,1}     transform input data to obtain desired sign for B0 on the output, default=0 uses input
      --cocos_in {1,2,3,4,5,6,7,8,11,12,13,14,15,16,17,18}
                              coerced COCOS index, otherwise default=None computes COCOS in GEQDSK file [1,3,5,7]

*******************
 Example eqdsk2ids
*******************

   .. code-block:: bash

      $ eqdsk2ids -s 134174 -r 117 -g /home/ITER/sawantp1/git/idstools/tests/geqdsk/example.gfile -u sawantp1 -d ITER --log INFO
      24/03/20 17:19:44 INFO: loading GEQDSK file ...
      24/03/20 17:19:44 INFO: GEQDSK COCOS:
      { 'COCOS': 1,
      'sigma_Ip': -1.0,
      'sigma_B0': -1.0,
      'exp_Bp': 0,
      'sigma_Bp': 1,
      'sigma_RphiZ': 1,
      'sigma_rhothetaphi': 1,
      'sign_q_pos': 1,
      'sign_pprime_pos': -1,
      'theta_sign_clockwise': 1}
      24/03/20 17:19:44 INFO: GEQDSK Transformation Coeff.:
      { 'sigma_Ip_eff': 1.0,
      'sigma_B0_eff': 1.0,
      'sigma_Bp_eff': 1.0,
      'sigma_rhothetaphi_eff': 1.0,
      'sigma_RphiZ_eff': 1.0,
      'exp_Bp_eff': 1.0,
      'fact_psi': 6.283185307179586,
      'fact_q': 1.0,
      'fact_dpsi': 0.15915494309189535,
      'fact_dtheta': 1.0}
      24/03/20 17:19:44 INFO: mapping GEQDSK to IDS/equilibrium ...
      24/03/20 17:19:44 INFO: IDS COCOS:
      { 'COCOS': 11,
      'exp_Bp': 1,
      'sigma_B0': -1,
      'sigma_Bp': 1,
      'sigma_Ip': -1,
      'sigma_RphiZ': 1,
      'sigma_rhothetaphi': 1,
      'sign_pprime_pos': -1,
      'sign_q_pos': 1,
      'theta_sign_clockwise': 1}
      24/03/20 17:19:44 INFO: creating output datafile ...
      24/03/20 17:19:44 INFO: IDS/equilibrium populated in shot/run = 134174/117.

   .. code-block:: bash

      # Command Line Interface for EQDSK Convertor (eqdsk2ids)
      # Usage:
      # 0) Load IMAS and install fortranformat and Cerberus (if not done before)
      # 1) Compute COCOS and create IDS data file in local database
      $ eqdsk2ids -g path_to_gfile -s 12345 -r 1 -u userid -d ITER

      # 2) Enforce signs of Ip and/or B0 in output
      $ eqdsk2ids -g path_to_gfile -s 12345 -r 1 -u userid -d ITER --ipsign -1 --b0sign -1

      # 3) Increase verbosity to see information as COCOS index and transformation coeff.
      $ eqdsk2ids -g path_to_gfile -s 12345 -r 1 -u userid -d ITER --log INFO

      # 4) Coerce input COCOS index
      $ eqdsk2ids -g path_to_gfile -s 12345 -r 1 -u userid -d ITER --cocos_in 7

   .. code-block:: python

      # Functional Interface in Python (database_tools/eqdsk2ids.py)
      # Usage:
      # 0) Initialization
      from database_tools.eqdsk2ids import eqdsk2ids

      # 1) Convert Gfile
      eq = eqdsk2ids(gfile="path/to/gfile")

      # 2) Convert Gfile and alter signs both for Ip & B0
      eq = eqdsk2ids(gfile="path/to/gfile", ipsign=-1, b0sign=-1)

      # 3) Convert Gfile with COCOS input (=1) coerced
      eq = eqdsk2ids(gfile="path/to/gfile", cocos_in=1)
