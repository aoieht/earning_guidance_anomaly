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
forecast_level = pd.pivot_table(earning_forecast_data,index='证券代码',columns='报告期',values='平均预告增幅',aggfunc='first') #业绩预告平均预告增幅表

forecast_level_re = pd.DataFrame(data=None,columns=['Earning Forecast Level'],index=event_sample.index) #按事件样本作匹配

for e in range(len(event_sample)):
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_fy = pd.to_datetime(event_sample.iloc[e]['会计年度'])
        tmp_level = forecast_level.loc[tmp_stock,tmp_fy]
        forecast_level_re.at[event_sample.index[e],'Earning Forecast Level (%)'] = tmp_level
            
    except:
        continue
    
exceldata = forecast_level_re
exceldata.to_excel('event_earning_forecast_level.xlsx')