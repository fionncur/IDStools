###########
 eqdsk2ids
###########

*eqdsk2ids* EQDSK Convertor allows users to specify a destination URI, a GEQDSK file path, 
logging levels, and Tokamak coordinate conventions for converting GEQDSK file to equilibrium IDS

******************
 Syntax eqdsk2ids
******************

   .. command-output:: eqdsk2ids -h

Example eqdsk2ids
~~~~~~~~~~~~~~~~~

   .. code-block:: bash

         $ eqdsk2ids -c 11 -g resources/geqdsk/example.gfile --dest "imas:hdf5?user=sawantp1;pulse=134174;run=117;database=ITER;version=3" --log INFO
         24/10/30 16:38:16 INFO: loading GEQDSK file ...
         24/10/30 16:38:16 INFO: GEQDSK COCOS: 
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
         24/10/30 16:38:16 INFO: GEQDSK Transformation Coeff.: 
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
         24/10/30 16:38:16 INFO: mapping GEQDSK to IDS/equilibrium ...
         24/10/30 16:38:16 INFO: IDS COCOS: 
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
         24/10/30 16:38:16 INFO: creating output datafile ...
         24/10/30 16:38:16 INFO: IDS/equilibrium populated in  sdcc-login04.iter.org:imas:hdf5?user=sawantp1;pulse=134174;run=117;database=ITER;version=3 .