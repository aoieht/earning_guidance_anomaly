#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 13:15:37 2018

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

#导入融券信息数据
shortable_path = '../raw_data/historical_short_selling_info.xlsx'
shortable_data = pd.read_excel(shortable_path).set_index('证券代码')

shortable = pd.DataFrame(data=None,index=event_sample.index,columns=['Shortable'])

for e in range(len(event_sample)): #按事件作匹配
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_event_date = pd.to_datetime(event_sample.iloc[e]['预计披露日期'])        
        if tmp_stock not in shortable_data.index: #构建Shortable dummy variable
            shortable.iloc[e] = 0
        elif tmp_event_date > shortable_data.loc[tmp_stock]['生效起始日']:
            shortable.iloc[e] = 1
        elif tmp_event_date <= shortable_data.loc[tmp_stock]['生效起始日']:
            shortable.iloc[e] = 0

    except:
        continue
    
exceldata = shortable
exceldata.to_excel('event_shortable.xlsx')