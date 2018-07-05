#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 13:37:09 2018

@author: shujian
"""


import pandas as pd
import numpy as np
from numpy.linalg import inv
from datetime import timedelta

#导入事件样本
event_path = '../raw_data/event_sample.xlsx'
event_sample = pd.read_excel(event_path)
event_sample = event_sample.set_index(event_sample['股票代码'].map(str)+'@'+event_sample['会计年度'])

#导入业绩预告信息样本
earning_forecast_path = '../raw_data/historical_earning_forecast.xlsx'
earning_forecast_data = pd.read_excel(earning_forecast_path)
forecast_type = pd.pivot_table(earning_forecast_data,index='证券代码',columns='报告期',values='预警类型',aggfunc='first') #业绩预告类型表

tmp_columns = earning_forecast_data['预警类型'].unique()
forecast_type_re = pd.DataFrame(data=None,columns=tmp_columns,index=event_sample.index) #按事件样本作匹配

for e in range(len(event_sample)):
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_fy = pd.to_datetime(event_sample.iloc[e]['会计年度'])
        tmp_type = forecast_type.loc[tmp_stock,tmp_fy]
        if tmp_type in forecast_type_re.columns: #构建dummy variable
            forecast_type_re.iloc[e][tmp_type] = 1
            forecast_type_re.iloc[e] = forecast_type_re.iloc[e].fillna(0)
        else:    
            continue
            
    except:
        continue
    
exceldata = forecast_type_re
exceldata.to_excel('event_earning_forecast_type.xlsx')