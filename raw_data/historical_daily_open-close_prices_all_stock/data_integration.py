# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np

daily_p_data = None

for year in range(2010, 2017):
    tmp_path = str(year)+'.xlsx'
    tmp_data = pd.read_excel(tmp_path)
    daily_p_data = pd.concat([daily_p_data, tmp_data], axis=0)
    
tmp_table_open = pd.pivot_table(daily_p_data, index=['交易日'], columns=['股票代码'], values='开盘价', aggfunc=np.mean)
tmp_table_close = pd.pivot_table(daily_p_data, index=['交易日'], columns=['股票代码'], values='收盘价', aggfunc=np.mean)

save_path = pd.ExcelWriter('daily_price.xlsx')
tmp_table_open.to_excel(save_path,'open price')
tmp_table_close.to_excel(save_path,'close price')
save_path.save()