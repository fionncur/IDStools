echo -e "105033 1 =======================================================================================\n\n"
# 105033 1 ITER 7.5MA H-DINA2022 PFPO1-5a            -7.5   -2.65  H  Ohmic  DINA-IMAS  2022-12-16 16:42:38 CORE-PASS No edge
python scripts/idscompo.py -s 105033 -r 1
ids_compo -s 105033 -r 1
echo -e "131047 7=======================================================================================\n\n"
#131047 7 ITER FPO Q=3,tauF=2tauE                  -15.0  -5.3   D-T H-mode ASTRA      2022-11-30 12:23:05 CORE-PASS No edge
python scripts/idscompo.py -s 131047 -r 7
ids_compo -s 131047 -r 7
echo -e "130012 4=======================================================================================\n\n"
#130012 4 ITER ITER-baseline-DT_more_stable_q95>2  -15 -5.3 D-T  H-L-H      METIS   2022-09-13 09:28:20 CORE-PASS No edge
python scripts/idscompo.py -s 130012 -r 4
ids_compo -s 130012 -r 4
echo -e "123276  1=======================================================================================\n\n"
# 123276  1 ITER NME2022Kaveeva with Be top-puff D1p25e23_Ne0p35e20   -15.02 -5.3   D  tbd SOLPS-ITER 2022-07-28 18:57:27 CORE-PASS Edge Pass
python scripts/idscompo.py -s 123276 -r 1
ids_compo -s 123276 -r 1
echo -e "130506  403=======================================================================================\n\n"
# 130506  403  ITER      Baseline-DT, 15MA 5.3T L-H-L, 49.7MW Paux, Be/W, P   -15.0  -5.3   D-T L-H-L  CORSICA 2022-06-23 10:02:18 NO PASS issue of reading equillibrium ids No edge
python scripts/idscompo.py -s 130506 -r 403
ids_compo -s 130506 -r 403
echo -e "130507  3=======================================================================================\n\n"
# 130507  3    ITER      Hybrid-DT, 11.5MA 5.3T L-H-L, 73.0MW Paux, Be/W      -11.5  -5.3   D-T L-H-L  CORSICA 2022-06-23 10:02:24 NO PASS issue of reading equillibrium ids No edge
python scripts/idscompo.py -s 130507 -r 3
ids_compo -s 130507 -r 3
echo -e "22578  1=======================================================================================\n\n"
# 22578  1    ITER      F57-120-N_1.2%-Be0,D_tpt=2.23e23,N_tpt=1.10e21       -15.02 -5.3   D tbd SOLPS4.3  2022-06-10 17:04:50 CORE PASS File error
python scripts/idscompo.py -s 22578 -r 1
ids_compo -s 22578 -r 1
echo -e "123170  2=======================================================================================\n\n"
# 123170  2    ITER      D+He+Ne_130MW_Be-top_cNe=0.4%_Dtpt=1.76e21_f/4       -10.05 -5.3   D tbd SOLPS-ITER 2022-06-10 17:24:31 CORE-PASS no edge
python scripts/idscompo.py -s 123170 -r 2
ids_compo -s 123170 -r 2
echo -e "104010  2=======================================================================================\n\n" 
# 104010  2    ITER   OPE1057 - Three ion ICRH scheme IMAS run -8.8   -3.13  H         L-mode JETTO mkimas  2022-06-09 17:36:27 CORE-PASS no edge
python scripts/idscompo.py -s 104010 -r 2
ids_compo -s 104010 -r 2
echo -e "125001  5=======================================================================================\n\n"
# 125001  5    ITER      10MA D-DINA2019-02 -10.1  -5.3   D         L-mode           DINA 2021-11-13 00:28:18 NO CORE
python scripts/idscompo.py -s 125001 -r 2
ids_compo -s 125001 -r 2
echo -e "104105  12=======================================================================================\n\n"
# 104105  12   ITER      Emmi H 7.5MA 2.65T with He, L-H transition -15.0  -5.3   H  L-mode           JINTRAC mkimas + spider-inverse  2021-09-29 15:12:54 CORE-PASS
python scripts/idscompo.py -s 104105 -r 12
ids_compo -s 104105 -r 12
echo -e "114102  22=======================================================================================\n\n"
# 114102  22   ITER      Vasilli He 5.0MA 1.8T L-H transition -5.0   -1.8   He4  H-mode  JINTRAC mkimas + spider-inverse  2021-09-29 15:12:54 CORE-PASS no edge
python scripts/idscompo.py -s 114102 -r 22
ids_compo -s 114102 -r 22
echo -e "120014  1=======================================================================================\n\n" 
# 120014  1    iter      D_Plasma_50%_Greenwald_Half_field  -7.5   -2.83  D H-L-H  METIS alone 2021-05-18 11:05:49 CORE-PASS But Density error no edge
python scripts/idscompo.py -s 120014 -r 1
ids_compo -s 120014 -r 1
echo -e "104101  1=======================================================================================\n\n" 
# 104101  1    iter      F4E-GRT502 derived H 9.5MA 4.5T 20MW L-mode -9.5   -4.5   H  L-mode JINTRAC mkimas  2020-04-07 12:55:01 CORE PASS
python scripts/idscompo.py -s 104101 -r 1
ids_compo -s 104101 -r 1
echo -e "134110  110=======================================================================================\n\n"
# 134110  110  iter      H-L trans. DT 15MA 5.3T, high Prad_W, 20s EC ramp -15.0  -5.3   T-D H-mode JINTRAC 2020-04-24 14:13:27 CORE PASS
python scripts/idscompo.py -s 134110 -r 110
ids_compo -s 134110 -r 110
echo -e "125501  2=======================================================================================\n\n"
# 125501  2    ITER      ITER#1514_i-dib-0903-00d_low-n_T-10  -15.0  -5.3   D L-mode DIVIMP 020-07-23 21:04:55
python scripts/idscompo.py -s 125501 -r 2
ids_compo -s 125501 -r 2
echo -e "================================DONE=======================================================\n\n"




