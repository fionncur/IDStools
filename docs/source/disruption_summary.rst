####################
 disruption_summary
####################

Script to list available disruptions in a specific folder

***************************
 Syntax disruption_summary
***************************

  .. command-output:: disruption_summary -h
    
****************************
 Example disruption_summary
****************************

   .. code:: bash

      $ disruption_summary
      ----> Default call equivalent to:
            disruption_summary -c shot,run,ip,b0,ne0,dis_type,VD_dir,IREmax,HF,workflow,ref_name
      ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Pulse   Run  Ip[MA]  B0[T]  ne0[m-3]  Type          VD    I_RE_max[MA]  HF    Workflow                        Reference
      ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
      100021  1     -7.5   -2.65  5e+19     VDE           up    0.0           0.2   DINA ITER Disruption Simulator  DINA-20/MD_VDE_10_7.5MA_2.65T/VDE7.5_up_Be3_chi4_5_19
      100022  1     -7.5   -2.65  5e+19     MD            up    0.0           0.2   DINA ITER Disruption Simulator  DINA-20/MD_VDE_10_7.5MA_2.65T/MD7.5_up_Be3_chi1_5_19
      100023  1     -7.5   -2.65  5e+19     VDE           down  0.0           1.33  DINA ITER Disruption Simulator  DINA-20/MD_VDE_10_7.5MA_2.65T/VDE7.5_dw_Be0_chi1_5_19
      100027  1     -7.5   -2.65  5e+19     VDE           up    0.0           0.26  DINA ITER Disruption Simulator  DINA-20/MD_VDE_10_7.5MA_2.65T/VDE7.5_up_Be1_chi4_5_19
