#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 22:17:33 2018

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
report_date = pd.pivot_table(event_sample, index=['股票代码'], columns='会计年度', values='预计披露日期', aggfunc='first')

#导入分析师业绩预测数据
earning_forecast_data_path = '../raw_data/historical_daily_EPS_forcast_all_stock/average_daily_EPS_forecast.xlsx'
earning_forecast = pd.read_excel(earning_forecast_data_path).set_index('日期')

#导入实际业绩数据
actual_earning_data_path = '../raw_data/historical_annually_diluted_EPS_all_stock.xlsx'
actual_earning = pd.read_excel(actual_earning_data_path)
actual_earning = pd.pivot_table(actual_earning, index=['Stkcd'], columns='FY', values='diluted_eps', aggfunc=np.mean)

#导入股票日度价格数据
price_data_path = '../raw_data/historical_daily_open-close_prices_all_stock/daily_price.xlsx'
close_price = pd.read_excel(price_data_path,'close price')
close_price = close_price.set_index(pd.to_datetime(close_price['交易日']))



earning_surprise = pd.DataFrame(data=None, index=report_date.index, columns=report_date.columns) #构建Earning Surprise dummy variable
earning_surprise_level = pd.DataFrame(data=None, index=report_date.index, columns=report_date.columns) #构建Earning Surprise level variable

for ro in range(report_date.shape[0]):
    for co in range(report_date.shape[1]):
        try:
            tmp_report_date = pd.to_datetime(report_date.iloc[ro,co])
            tmp_feps_series = earning_forecast.loc[:,report_date.index[ro]].to_frame().dropna()
            tmp_feps_series = tmp_feps_series.set_index(pd.to_datetime(tmp_feps_series.index)) #针对当前个股的分析师预测业绩序列
            tmp_price_series = close_price.loc[:,report_date.index[ro]].to_frame().dropna() #当前个股的历史日度收盘价
            tmp_eps_forecast = np.mean(tmp_feps_series[(tmp_feps_series.index < tmp_report_date) &  (tmp_feps_series.index >= (tmp_report_date-timedelta(days=90)))].values) #公告日前90天内分析师业绩预测平均值
            tmp_avg_price = np.mean(tmp_price_series[(tmp_price_series.index < tmp_report_date) &  (tmp_price_series.index >= (tmp_report_date-timedelta(days=90)))].values) #公告日前90天内日度收盘价平均值
            earning_surprise_level.iloc[ro,co] = (actual_earning.loc[report_date.index[ro],pd.to_datetime(report_date.columns[co])] - tmp_eps_forecast)/tmp_avg_price #当前时间Earning Surprise level
            if actual_earning.loc[report_date.index[ro]][pd.to_datetime(report_date.columns[co])] > tmp_eps_forecast: #构建Earning Surprise dummy variable
                earning_surprise.iloc[ro,co] = 1
            elif actual_earning.loc[report_date.index[ro]][pd.to_datetime(report_date.columns[co])] <= tmp_eps_forecast:
                earning_surprise.iloc[ro,co] = 0
            else:
                continue
                
        except:
            continue

earning_surprise_re = pd.DataFrame(data=None, index=event_sample.index, columns=['Earning Surprise_Dummy','Earning Surprise_Level']) #按事件样本作匹配
for i in range(len(earning_surprise_re)):
    earning_surprise_re.iloc[i]['Earning Surprise_Dummy'] = earning_surprise.loc[event_sample.iloc[i]['股票代码']][event_sample.iloc[i]['会计年度']]
    earning_surprise_re.iloc[i]['Earning Surprise_Level'] = earning_surprise_level.loc[event_sample.iloc[i]['股票代码']][event_sample.iloc[i]['会计年度']]

    
exceldata = earning_surprise_re
exceldata.to_excel('event_earning_surprise.xlsx')