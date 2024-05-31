###########
 eqdsk2ids
###########

*eqdsk2ids* EQDSK Convertor

******************
 Syntax eqdsk2ids
******************

   .. command-output:: eqdsk2ids -h

Example eqdsk2ids
~~~~~~~~~~~~~~~~~

   .. code-block:: bash

        $ eqdsk2ids -c 11 -p 134174 -r 117 -c 11 -g resources/geqdsk/example.gfile -u <username> -d ITER --log INFO   
        $ eqdsk2ids -c 11 --uri "imas:mdsplus?user=username;pulse=134174;run=117;database=ITER;version=3" -g resources/geqdsk/example.gfile --log INFO
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
        24/03/20 17:19:44 INFO: IDS/equilibrium populated in pulse/run = sdcc-login01.iter.org:/home/ITER/username/public/imasdb/ITER/3 (pulse 134174,117 ).

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

      # Functional Interface in Python (idstools/eqdsk2ids.py)
      # Usage:
      # 0) Initialization
      from idstools.eqdsk2ids import eqdsk2ids

      # 1) Convert Gfile
      eq = eqdsk2ids(gfile="path/to/gfile")

      # 2) Convert Gfile and alter signs both for Ip & B0
      eq = eqdsk2ids(gfile="path/to/gfile", ipsign=-1, b0sign=-1)

      # 3) Convert Gfile with COCOS input (=1) coerced
      eq = eqdsk2ids(gfile="path/to/gfile", cocos_in=1)
