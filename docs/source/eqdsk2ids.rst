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

         $ eqdsk2ids -c 11 -g resources/geqdsk/example.gfile --dest \"imas:hdf5?user=$USER;pulse=134174;run=117;database=ITER;version=3?path=$DATABASE_DIR\" --log INFO"

         24/10/18 16:35:52 INFO: loading GEQDSK file ...
         24/10/18 16:35:52 INFO: GEQDSK COCOS: 
         { 'COCOS': 11,
         'sigma_ip': -1.0,
         'sigma_b0': -1.0,
         'exp_bp': 1,
         'sigma_bp': 1,
         'sigma_rphi_z': 1,
         'sigma_rhothetaphi': 1,
         'sign_q_pos': 1,
         'sign_pprime_pos': -1,
         'theta_sign_clockwise': 1}
         24/10/18 16:35:52 INFO: GEQDSK Transformation Coeff.: 
         { 'sigma_Ip_eff': 1.0,
         'sigma_B0_eff': 1.0,
         'sigma_Bp_eff': 1.0,
         'sigma_rhothetaphi_eff': 1.0,
         'sigma_RphiZ_eff': 1.0,
         'exp_Bp_eff': 0.0,
         'fact_psi': 1.0,
         'fact_q': 1.0,
         'fact_dpsi': 1.0,
         'fact_dtheta': 1.0}
         24/10/18 16:35:52 INFO: mapping GEQDSK to IDS/equilibrium ...
         16:35:52 INFO     Parsing data dictionary version 3.42.0 @dd_zip.py:166
         24/10/18 16:35:52 INFO: Parsing data dictionary version 3.42.0
         24/10/18 16:35:53 INFO: IDS COCOS: 
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
         24/10/18 16:35:53 INFO: creating output datafile ...
         24/10/18 16:35:53 INFO: IDS/equilibrium populated in  sdcc-login04.iter.org:imas:hdf5?user=sawantp1;pulse=134174;run=117;database=ITER;version=3 .
