#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 20:36:20 2018

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

#导入市值数据
mkt_cap_path = '../raw_data/historical_monthly_market_capital.xlsx'
market_cap_data = pd.read_excel(mkt_cap_path)
market_cap = pd.pivot_table(market_cap_data,index='Trdmnt',columns='Stkcd',values='lnMV')

market_cap_re = pd.DataFrame(data=None,index=event_sample.index,columns=['ln(Market_Cap)'])

for e in range(len(event_sample)): #按事件做匹配
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_event_month = pd.to_datetime(event_sample.iloc[e]['预计披露日期']).strftime('%Y-%m')
        tmp_lnmv_series = market_cap.loc[:,tmp_stock].dropna()
        tmp_loc = tmp_lnmv_series.index.get_loc(tmp_event_month)
        market_cap_re.iloc[e]['ln(Market_Cap)'] = tmp_lnmv_series.iloc[tmp_loc-1]
    except:
        continue
    
exceldata = market_cap_re
exceldata.to_excel('event_market_capital.xlsx')