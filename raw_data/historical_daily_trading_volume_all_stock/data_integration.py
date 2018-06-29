# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np

daily_v_data = None

for year in range(2010, 2017):
    tmp_path = str(year)+'.xlsx'
    tmp_data = pd.read_excel(tmp_path)
    daily_v_data = pd.concat([daily_v_data, tmp_data], axis=0)
    
tmp_table = pd.pivot_table(daily_v_data, index=['Trddt'], columns=['Stkcd'], values='Dnshrtrd', aggfunc=np.sum)
save_path = 'daily_trading_volume.xlsx'
tmp_table.to_excel(save_path)