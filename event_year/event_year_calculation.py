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


tmp_columns = pd.to_datetime(event_sample['会计年度']).dt.strftime('%Y').unique()
year = pd.DataFrame(data=None,columns=tmp_columns,index=event_sample.index)

for e in range(len(event_sample)):
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_fy = pd.to_datetime(event_sample.iloc[e]['会计年度']).strftime('%Y')
        if tmp_fy in year.columns: #事件会计年度转dummy variable
            year.iloc[e][tmp_fy] = 1
            year.iloc[e] = year.iloc[e].fillna(0)
        else:    
            continue
            
    except:
        continue
    
exceldata = year
exceldata.to_excel('event_year.xlsx')