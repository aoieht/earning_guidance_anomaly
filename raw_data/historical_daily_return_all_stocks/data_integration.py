# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np

daily_r_data = None

for year in range(2006, 2017):
    tmp_path = str(year)+'.xlsx'
    tmp_data = pd.read_excel(tmp_path)
    daily_r_data = pd.concat([daily_r_data, tmp_data], axis=0)
    
tmp_table = pd.pivot_table(daily_r_data, index=['Trddt'], columns=['Stkcd'], values='Dretnd', aggfunc=np.sum)
save_path = 'daily_return.xlsx'
tmp_table.to_excel(save_path)