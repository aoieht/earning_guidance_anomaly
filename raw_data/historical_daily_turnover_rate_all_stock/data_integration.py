# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np

daily_tr_data = None

for i in range(1, 6):
    tmp_path = 'TurnoverRate'+str(i)+'.xlsx'
    tmp_data = pd.read_excel(tmp_path)
    daily_tr_data = pd.concat([daily_tr_data, tmp_data], axis=0)
    
tmp_table = pd.pivot_table(daily_tr_data, index=['日期_Date'], columns=['股票代码_Stkcd'], values='流通股日换手率(%)_DTrdTurnR', aggfunc=np.sum)
save_path = 'daily_turnover_rate.xlsx'
tmp_table.to_excel(save_path)