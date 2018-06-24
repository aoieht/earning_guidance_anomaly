#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 13:20:13 2018

@author: aoieht
"""

import pandas as pd
import numpy as np
from numpy.linalg import inv
from datetime import timedelta

event_path = '../raw_data/event_sample.xlsx'
return_data_path = '../raw_data/historical_daily_return_with_div_all_stocks/daily_return_with_div.xlsx'
r_f_data_path = '../raw_data/historical_daily_risk-free_rate.xlsx'
factors_data_path = '../raw_data/historical_daily_Fama-French_three_factors_value.xlsx'

event_sample = pd.read_excel(event_path)
event_sample = event_sample.set_index(event_sample['股票代码'].map(str)+'@'+event_sample['会计年度'])

daily_return = pd.read_excel(return_data_path).set_index('Trddt')
r_f_data = pd.read_excel(r_f_data_path).set_index('Clsdt')
factors_data = pd.read_excel(factors_data_path).set_index('TradingDate')

tmp_columns = []
for i in range(-10, 11):
    tmp_columns.append('t_'+str(i))
ab_r = pd.DataFrame(data=None, index=event_sample.index, columns=tmp_columns)

for e in range(len(event_sample)):
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_event_date = pd.to_datetime(event_sample.iloc[e]['预计披露日期'])
        if tmp_event_date.isoweekday() == 6:
            tmp_event_date = (tmp_event_date + timedelta(days=2)).strftime('%Y-%m-%d')
        elif tmp_event_date.isoweekday() == 7:
            tmp_event_date = (tmp_event_date + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            tmp_event_date = (tmp_event_date).strftime('%Y-%m-%d')
            
        tmp_r_series = daily_return.loc[:,tmp_stock].dropna()
        tmp_loc = tmp_r_series.index.get_loc(tmp_event_date)
        est_window_r = tmp_r_series.iloc[tmp_loc-221:tmp_loc-21]
        est_window_rf = r_f_data.loc[est_window_r.index]
        est_window_factors = factors_data.loc[est_window_r.index]
        est_const = pd.DataFrame(1, index=est_window_r.index, columns=['const'])
        X = pd.concat([est_const, est_window_rf, est_window_factors], axis=1).fillna(0).as_matrix()
        beta_hat = np.matmul(np.matmul(inv(np.matmul(np.transpose(X), X)), np.transpose(X)), est_window_r.fillna(0).as_matrix())
        eva_window_r = tmp_r_series.iloc[tmp_loc-10:tmp_loc+11]
        eva_window_rf = r_f_data.loc[eva_window_r.index]
        eva_window_factors = factors_data.loc[eva_window_r.index]
        eva_const = pd.DataFrame(1, index=eva_window_r.index, columns=['const'])
        X = pd.concat([eva_const, eva_window_rf, eva_window_factors], axis=1).fillna(0).as_matrix()
        r_hat = np.matmul(X, beta_hat)
        ab_r.iloc[e] = np.transpose(eva_window_r.fillna(0).as_matrix() - r_hat)
    except:
        continue
car = np.sum(ab_r.loc[:,['t_-5','t_-4','t_-3','t_-2','t_-1']], axis=1).to_frame(name='CAR_[-5,-1]').replace(to_replace=0,value=np.nan)
exceldata = pd.concat([ab_r,car],axis=1)
exceldata.to_excel('event_window_daily_abnormal_return.xlsx')