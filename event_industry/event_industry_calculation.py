#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 14:09:40 2018

@author: aoieht
"""

import pandas as pd
import numpy as np
from numpy.linalg import inv
from datetime import timedelta

#导入事件样本
event_path = '../raw_data/event_sample.xlsx'
event_sample = pd.read_excel(event_path)
event_sample = event_sample.set_index(event_sample['股票代码'].map(str)+'@'+event_sample['会计年度'])

#导入行业信息数据
earning_forecast_path = '../raw_data/historical_earning_forecast.xlsx'
earning_forecast_data = pd.read_excel(earning_forecast_path)
industry = pd.pivot_table(earning_forecast_data,index='证券代码',columns='报告期',values='Wind行业',aggfunc='first')

tmp_columns = earning_forecast_data['Wind行业'].unique()
industry_re = pd.DataFrame(data=None,columns=tmp_columns,index=event_sample.index)

for e in range(len(event_sample)): #按事件作匹配
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_fy = pd.to_datetime(event_sample.iloc[e]['会计年度'])
        tmp_industry = industry.loc[tmp_stock,tmp_fy]
        if tmp_industry in industry_re.columns:
            industry_re.iloc[e][tmp_industry] = 1
            industry_re.iloc[e] = industry_re.iloc[e].fillna(0)
        else:    
            continue
            
    except:
        continue
    
exceldata = industry_re
exceldata.to_excel('event_industry.xlsx')