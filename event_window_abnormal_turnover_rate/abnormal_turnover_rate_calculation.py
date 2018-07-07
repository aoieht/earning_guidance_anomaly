#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 11:07:39 2018

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

#导入个股日换手率数据
turnover_data_path = '../raw_data/historical_daily_turnover_rate_all_stock/daily_turnover_rate.xlsx'
daily_turnover = pd.read_excel(turnover_data_path).set_index('日期_Date')

#导入市场日换手率数据
mkt_turnover_path = '../raw_data/historical_daily_turnover_rate_all_stock/Market_TurnoverRate.xlsx'
mkt_turnover = pd.read_excel(mkt_turnover_path).set_index('日期')

tmp_columns = []
for i in range(-10, 11): #事件窗口列标签
    tmp_columns.append('t_'+str(i))
ab_tr = pd.DataFrame(data=None, index=event_sample.index, columns=tmp_columns)

for e in range(len(event_sample)):
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_event_date = pd.to_datetime(event_sample.iloc[e]['预计披露日期'])
        if tmp_event_date.isoweekday() == 6: #公告日为周末的调整为交易日
            tmp_event_date = (tmp_event_date + timedelta(days=2)).strftime('%Y-%m-%d')
        elif tmp_event_date.isoweekday() == 7:
            tmp_event_date = (tmp_event_date + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            tmp_event_date = (tmp_event_date).strftime('%Y-%m-%d')
        
        tmp_tr_series = daily_turnover.loc[:,tmp_stock].dropna() #当前股票的日换手率序列
        tmp_loc = tmp_tr_series.index.get_loc(tmp_event_date)
        
        #非事件窗口: [t_0 - 135, t_0 - 11]与[t_0 + 11, t_0 + 135]之并
        nonevent_window_tr = tmp_tr_series.iloc[np.r_[tmp_loc-135:tmp_loc-10,tmp_loc+11:tmp_loc+136]]
        nonevent_window_mkttr = mkt_turnover.loc[nonevent_window_tr.index]
        
        #事件窗口: [t_0 - 10, t_0 + 10]
        event_window_tr = tmp_tr_series.iloc[tmp_loc-10:tmp_loc+11]
        event_window_mkttr = mkt_turnover.loc[event_window_tr.index]
        
        tmp_abtr = (event_window_tr.values - np.transpose(event_window_mkttr.values)) - np.nanmean(nonevent_window_tr.values - np.transpose(nonevent_window_mkttr.values)) #事件窗口日度abnormal turnover rate
        ab_tr.iloc[e] = tmp_abtr
    except:
        continue
    
catr = np.sum(ab_tr.loc[:,['t_-5','t_-4','t_-3','t_-2','t_-1']], axis=1).to_frame(name='CATR_[-5,-1]').replace(to_replace=0,value=np.nan) #事件日前5交易日的累计abnormal turnover rate记CATR
exceldata = pd.concat([ab_tr,catr],axis=1)
exceldata.to_excel('event_window_daily_abnormal_turnover_rate.xlsx')