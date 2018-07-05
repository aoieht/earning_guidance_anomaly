import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear

reg CAR_51_ZH D_p
est store reg1
reg CAR_51_ZH D_p IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz 
est store reg2
reg CAR_51_ZH  D_pi  D_c2 D_c3 D_c4 D_pd
est store reg3
reg CAR_51_ZH D_pi  D_c2 D_c3 D_c4 D_pd IdioRisk  D_pi_IdioRisk D_pd_IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz 
est store reg4

esttab reg1 reg2 reg3 reg4, ar2 star(* 0.1 ** 0.05 *** 0.01), using aux_result1.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-preinc.xlsx", sheet("preinc") firstrow clear

reg CAR_51_ZH D_EPS
est store reg1
reg CAR_51_ZH D_EPS IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using aux_result2.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear
reg CAR_51_ZH CAT
est store reg1
reg CAR_51_ZH CAT IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using aux_result3.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-preinc.xlsx", sheet("preinc") firstrow clear
reg CAR_51_ZH CAT
est store reg1
reg CAR_51_ZH CAT IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using aux_result4.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear

reg CAT  D_pi  D_c2 D_c3 D_c4 D_pd
est store reg3
reg CAT D_pi  D_c2 D_c3 D_c4 D_pd Attention IdioRisk D_pi_IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz 
est store reg4

esttab reg3 reg4, ar2 star(* 0.1 ** 0.05 *** 0.01), using aux_result5.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-preinc.xlsx", sheet("preinc") firstrow clear
reg CAR_51_ZH Shortable
est store reg1
reg CAR_51_ZH Shortable IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using aux_result6.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear
reg CAR_51_ZH D_exppre if D_p==1
est store reg1
reg CAR_51_ZH D_exppre IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz if D_p==1
est store reg2
reg CAR_51_ZH D_exppre if D_pi==1
est store reg3
reg CAR_51_ZH D_exppre IdioRisk logMV Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz if D_pi==1
est store reg4

esttab reg1 reg2 reg3 reg4, ar2 star(* 0.1 ** 0.05 *** 0.01), using aux_result7.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-CAR_2.xlsx", sheet("CAR_2") firstrow clear
reg  rltnetinflow_S real_g relativerealg 
est store reg1
reg  rltnetinflow_S real_g relativerealg logMV Attention Momentum Momentum_3 D_2012-D_2016 D_cjy-D_zz
est store reg2
reg  rltnetinflow_S real_g relativerealg if D_pi==1
est store reg3
reg  rltnetinflow_S real_g relativerealg logMV Attention Momentum Momentum_3 D_2012-D_2016 D_cjy-D_zz if D_pi==1
est store reg4
esttab reg1 reg2 reg3 reg4, ar2 star(* 0.1 ** 0.05 *** 0.01), using aux_result8.csv

import excel "\\Mac\iCloud\Thesis by Shujian\allsample-preinc.xlsx", sheet("preinc") firstrow clear
reg CAT logMV
est store reg1
reg CAT logMV Attention IdioRisk  Momentum Momentum_3 ILLIQ D_2012-D_2016 D_cjy-D_zz 
est store reg2

esttab reg1 reg2, ar2 star(* 0.1 ** 0.05 *** 0.01), using aux_result9.csv
