#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 20:02:19 2018

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

#导入日度收益数据
return_data_path = '../raw_data/historical_daily_return_all_stocks/daily_return.xlsx'
daily_return = pd.read_excel(return_data_path).set_index('Trddt')

momentum = pd.DataFrame(data=None, index=event_sample.index, columns=['3-Month Momentum','12-Month Momentum'])

for e in range(len(event_sample)):
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_event_date = pd.to_datetime(event_sample.iloc[e]['预计披露日期'])
        if tmp_event_date.isoweekday() == 6: #公告日后最近交易日
            tmp_event_date = (tmp_event_date + timedelta(days=2)).strftime('%Y-%m-%d')
        elif tmp_event_date.isoweekday() == 7:
            tmp_event_date = (tmp_event_date + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            tmp_event_date = (tmp_event_date).strftime('%Y-%m-%d')
            
        tmp_r_series = daily_return.loc[:,tmp_stock].dropna()
        tmp_loc = tmp_r_series.index.get_loc(tmp_event_date)
        if tmp_loc >= 62:
            momentum.iloc[e]['3-Month Momentum'] = np.prod(np.add(1,tmp_r_series.iloc[tmp_loc-62:tmp_loc]))-1 #公告日前62个交易日的累计日度收益
            if tmp_loc >= 251:
                momentum.iloc[e]['12-Month Momentum'] = np.prod(np.add(1,tmp_r_series.iloc[tmp_loc-251:tmp_loc]))-1 #公告日前251个交易日的累计日度收益
            else:
                continue
        else:
            continue
    except:
        continue
    
exceldata = momentum
exceldata.to_excel('event_momentum.xlsx')
