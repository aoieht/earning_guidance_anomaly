# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np

daily_eps_expect_data = None

for year in range(2010, 2017):
    tmp_path = str(year)+'.xlsx'
    tmp_data = pd.read_excel(tmp_path)
    daily_eps_expect_data = pd.concat([daily_eps_expect_data, tmp_data], axis=0)
    
    
tmp_table = pd.pivot_table(daily_eps_expect_data, index=['日期'], columns='股票代码', values='预测EPS', aggfunc=np.mean)
save_path = 'average_daily_EPS_forecast.xlsx'
tmp_table.to_excel(save_path)