##################
 scenario_summary
##################

`scenario_summary` list available scenarios in a specific folder with
search facility

*************************
 Syntax scenario_summary
*************************

   .. command-output:: scenario_summary -h

**************************
 Example scenario_summary
**************************

.. code-block:: bash

   $ scenario_summary -s He4,2.65
   ----> Default call equivalent to:
       scenario_summary -c shot,run,database,ref_name,ip,b0,fuelling,confinement,workflow,date
   Pulse  Run Database                      Reference                      Ip[MA] B0[T]  Fuelling Confinement             Workflow                     Date
   110005  1    ITER    ITER-half-field-He4                                 -7.5   -2.65    He4      L-H-L     METIS                            2019-01-30 17:54:46
   110501  3    ITER    Nonactive-He, 7.5MA 2.65T L-H-L, 43.0MW Paux        -7.5   -2.65    He4      L-H-L     CORSICA                          2022-06-23 10:00:28
   110508  3    ITER    Nonactive-He, 7.5MA 2.65T L-mode, 28.3MW Paux       -7.5   -2.65    He4      L         CORSICA                          2022-06-23 10:01:09
   110509  3    ITER    Nonactive-He, 7.5MA 2.65T L-H-L, 43.0MW Paux        -7.5   -2.65    He4      L-H-L     CORSICA                          2022-06-23 10:01:14
   111000  60   ITER    PFPO-2 tf=tE,2NBI,highTped                          -7.5   -2.65    He4      H-mode    ASTRA                            2023-04-13 10:58:55
   111001  60   ITER    PFPO-2 tf=tE,2NBI,lowTped                           -7.5   -2.65    He4      H-mode    ASTRA                            2023-04-13 11:00:22
   113275  1    ITER    ITER#2360_(F57-40MW-He+5%H), MS-resolved            -7.51  -2.65    He4      tbd       SOLPS-ITER                       2022-06-10 14:34:07
   114100  51   iter    Pares He 7.5MA 20MW L-mode, DINA extr. equ. config  -7.5   -2.65    He4      L-mode    JINTRAC mkimas + SPIDER-inv      2020-10-27 00:47:16
   114101  41   iter    Vparail He 7.5MA 53MW H-mode, DINA extr. equ. conf  -7.5   -2.65    He4      H-mode    JINTRAC mkimas + SPIDER-inv      2020-10-27 00:32:47
   114103  13   ITER    Vasilli He 7.5MA 2.65T L-H transition               -7.5   -2.65    He4      L-mode    JINTRAC mkimas + spider-inverse  2023-02-10 14:14:48
   114103  23   ITER    Vasilli He 7.5MA 2.65T L-H transition               -7.5   -2.65    He4      H-mode    JINTRAC mkimas + spider-inverse  2023-02-10 14:14:56
   114103  33   ITER    Vasilli He 7.5MA 2.65T L-H transition               -7.5   -2.65    He4      H-mode    JINTRAC mkimas + spider-inverse  2023-02-10 14:15:04
   114103  43   ITER    Vasilli He 7.5MA 2.65T L-H transition               -7.5   -2.65    He4      H-mode    JINTRAC mkimas + spider-inverse  2023-02-10 14:15:12

.. code-block:: bash

   $ scenario_summary -s He4,2.65 -c shot,run,database,composition
   Pulse  Run Database                                    Composition X[ni/ne]
   131042  11   ITER    D(0.497),T(0.456),Be(0.020),He4(0.015),Ne(2.50e-03),Xe(2.65e-05),H(1.54e-05),W(7.02e-06)
   131042  12   ITER    D(0.497),T(0.456),Be(0.020),He4(0.015),Ne(2.50e-03),Xe(2.65e-05),H(1.54e-05),W(7.02e-06)

.. code-block:: bash

   $ scenario_summary -s He4 2.65
   ----> Default call equivalent to:
       scenario_summary -c shot,run,database,ref_name,ip,b0,fuelling,confinement,workflow,date
   Pulse  Run Database                      Reference                       Ip[MA] B0[T]  Fuelling   Confinement               Workflow                     Date
   100002  1    ITER    ITER-half-field-H                                   -7.5    -2.65   H       L-mode          METIS                            2019-01-30 17:54:38
   100501  3    ITER    Nonactive-H, 7.5MA 2.65T L-H-L, 46.8MW Paux         -7.5    -2.65   H       L-H-L           CORSICA                          2022-06-23 09:59:35
   100502  3    ITER    Nonactive-H, 7.5MA 2.65T L-H dithering, 39.2MW Pau  -7.5    -2.65   H       L-H dithering   CORSICA                          2022-06-23 09:59:52
   100503  3    ITER    Nonactive-H, 7.5MA 2.65T L-mode, 46.8MW Paux        -7.5    -2.65   H       L               CORSICA                          2022-06-23 09:59:59
   101000  60   ITER    PFPO-2 tf=tE,2NBI,highTped,postST                   -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 10:06:05
   101001  60   ITER    PFPO-2 tf=tE,2NBI,highTped,preST                    -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 10:07:26
   101002  60   ITER    PFPO-2 tf=tE,2NBI,lowTped,postST                    -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 10:08:46
   101003  60   ITER    PFPO-2 tf=tE,2NBI,lowTped,preST                     -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 10:10:09
   101004  70   ITER    PFPO-2 tf=2tE,2NBI                                  -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 10:11:59
   101005  70   ITER    PFPO-2 tf=tE,2NBI                                   -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 10:13:50
   101006  70   ITER    PFPO-2 tf=0.5tE,2NBI                                -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 10:15:39
   101013  10   ITER    PFPO-1 iterHH.HLBeEC stiff                          -7.5    -2.65   H       L-mode          ASTRA                            2023-04-13 15:01:22
   101014  10   ITER    PFPO-2 tf=tE,2NBI,lowTped,postST stiff              -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 15:02:47
   101014  11   ITER    PFPO-2 tf=tE,2NBI,lowTped,postST ETB10              -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 15:04:12
   101018  10   ITER    PFPO-1 iterHH.HLBeEC stiff NetoAr                   -7.5    -2.65   H       L-mode          ASTRA                            2023-04-13 14:07:42
   101019  10   ITER    PFPO-2 tf=tE,2NBI,lowTped,postST stiff NetoAr       -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 14:09:03
   101019  11   ITER    PFPO-2 tf=tE,2NBI,lowTped,postST ETB10 NetoAr       -7.5    -2.65   H       H-mode          ASTRA                            2023-04-13 14:10:27
   101020  10   ITER    PFPO-2 Profiles_0.5%He3                             -8.8    -3.13   H-He4   H-mode          ASTRA                            2023-04-13 10:22:11
   101021  10   ITER    PFPO-2 iterH3ion.3iNHHe                             -8.8    -3.13   H-He4   H-mode          ASTRA                            2023-04-13 10:24:12
