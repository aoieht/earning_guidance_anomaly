import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear

reg CAR_51 D_p, robust
est store reg1
reg CAR_51 D_p IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz, robust
est store reg2
reg CAR_51  D_pi  D_c2 D_c3 D_c4 D_pd, robust
est store reg3
reg CAR_51 D_pi  D_c2 D_c3 D_c4 D_pd IdioRisk  D_pi_IdioRisk D_pd_IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz, robust 
est store reg4

esttab reg1 reg2 reg3 reg4, ar2 star(* 0.1 ** 0.05 *** 0.01), using result1_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-preinc.xlsx", sheet("preinc") firstrow clear

reg CAR_51 D_EPS, robust
est store reg1
reg CAR_51 D_EPS IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz, robust 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using result2_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear
reg CAR_51 CAT, robust
est store reg1
reg CAR_51 CAT IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz, robust 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using result3_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-preinc.xlsx", sheet("preinc") firstrow clear
reg CAR_51 CAT, robust
est store reg1
reg CAR_51 CAT IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz, robust 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using result4_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear

reg CATR  D_pi  D_c2 D_c3 D_c4 D_pd, robust
est store reg3
reg CATR D_pi  D_c2 D_c3 D_c4 D_pd IdioRisk D_pi_IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz, robust
est store reg4

esttab reg3 reg4, ar2 star(* 0.1 ** 0.05 *** 0.01), using result5_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-preinc.xlsx", sheet("preinc") firstrow clear
reg CAR_51 Shortable, robust
est store reg1
reg CAR_51 Shortable IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz, robust 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using result6_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear
reg CAR_51 D_exppre if D_p==1, robust
est store reg1
reg CAR_51 D_exppre IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz if D_p==1, robust
est store reg2
reg CAR_51 D_exppre if D_pi==1, robust
est store reg3
reg CAR_51 D_exppre IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz if D_pi==1, robust
est store reg4

esttab reg1 reg2 reg3 reg4, ar2 star(* 0.1 ** 0.05 *** 0.01), using result7_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear
reg  rltnetinflow_S real_g relativerealg, robust 
est store reg1
reg  rltnetinflow_S real_g relativerealg logMV Momentum Momentum_3 D_2012-D_2016 D_cjy-D_zz, robust
est store reg2
reg  rltnetinflow_S real_g relativerealg if D_pi==1, robust
est store reg3
reg  rltnetinflow_S real_g relativerealg logMV Momentum Momentum_3 D_2012-D_2016 D_cjy-D_zz if D_pi==1, robust
est store reg4
esttab reg1 reg2 reg3 reg4, ar2 star(* 0.1 ** 0.05 *** 0.01), using result8_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-preinc.xlsx", sheet("preinc") firstrow clear
reg CAT logMV, robust
est store reg1
reg CAT logMV IdioRisk  Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz, robust 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using result9_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear
gen D_piIdioRisk = D_pi*IdioRisk
reg CAR_51 D_pi IdioRisk D_piIdioRisk if (D_pi==1 | D_npre==1), robust
est store reg1
reg CAR_51 D_pi IdioRisk D_piIdioRisk ILLIQ logMV Momentum Momentum_3 D_2012-D_2016 D_cjy-D_zz if (D_pi==1 | D_npre==1), robust
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using result10_rbst.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear
reg CAR_51 IdioRisk if D_pi==1, robust
est store reg1
reg CAR_51 IdioRisk ILLIQ logMV Momentum Momentum_3 D_2012-D_2016 D_cjy-D_zz if D_pi==1, robust
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using result11_rbst.csv
