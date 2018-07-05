#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 14:36:02 2018

@author: shujian
"""

import pandas as pd
import numpy as np
from numpy.linalg import inv
from datetime import timedelta

#导入历史事件样本
event_ref_path = '../raw_data/historical_report_date.xlsx'
event_ref_sample = pd.read_excel(event_ref_path)
event_ref_sample = event_ref_sample.set_index(event_ref_sample['StockID'].map(str) + '@' + event_ref_sample['FY'].dt.strftime('%Y-%m-%d'))

#导入事件样本
event_path = '../raw_data/event_sample.xlsx'
event_sample = pd.read_excel(event_path)
event_sample = event_sample.set_index(event_sample['股票代码'].map(str)+'@'+event_sample['会计年度'])

#导入股票日度收益数据
return_data_path = '../raw_data/historical_daily_return_all_stocks/daily_return.xlsx'
daily_return = pd.read_excel(return_data_path).set_index('Trddt')

#导入无风险收益率数据
r_f_data_path = '../raw_data/historical_daily_risk-free_rate.xlsx'
r_f_data = pd.read_excel(r_f_data_path).set_index('Clsdt')

#导入Fama-French三因子数据
factors_data_path = '../raw_data/historical_daily_Fama-French_three_factors_value.xlsx'
factors_data = pd.read_excel(factors_data_path).set_index('TradingDate')

#目标变量Abnormal Idiosyncratic Volatility
AIVol = pd.DataFrame(data=None, index=event_ref_sample.index, columns=['AIVol_[-1,1]','Stock','FY'])
AIVol_est = pd.DataFrame(data=None, index=event_sample.index, columns=['Estimated AIVol_[-1,1]'])


for e in range(len(event_ref_sample)):
    try:
        tmp_stock = event_ref_sample.iloc[e]['StockID']
        tmp_event_date = pd.to_datetime(event_ref_sample.iloc[e]['ReportDate'])
        tmp_fy = event_ref_sample.iloc[e]['FY'].strftime('%Y-%m-%d')
        if tmp_event_date.isoweekday() == 6: #调整周末公告日为交易日
            tmp_event_date = (tmp_event_date + timedelta(days=2)).strftime('%Y-%m-%d')
        elif tmp_event_date.isoweekday() == 7:
            tmp_event_date = (tmp_event_date + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            tmp_event_date = (tmp_event_date).strftime('%Y-%m-%d')
            
        tmp_r_series = daily_return.loc[:,tmp_stock].dropna()
        tmp_loc = tmp_r_series.index.get_loc(tmp_event_date)
        
        #估计窗口: [t_0 - 221, t_0 - 21]
        est_window_r = tmp_r_series.iloc[tmp_loc-221:tmp_loc-20]
        est_window_rf = r_f_data.loc[est_window_r.index]
        est_window_factors = factors_data.loc[est_window_r.index]
        est_const = pd.DataFrame(1, index=est_window_r.index, columns=['const'])
        X = pd.concat([est_const, est_window_rf, est_window_factors], axis=1).fillna(0).as_matrix()
        beta_hat = np.matmul(np.matmul(inv(np.matmul(np.transpose(X), X)), np.transpose(X)), est_window_r.fillna(0).as_matrix()) #OLS得到三因子的risk loading
        
        #非事件窗口: [t_0 - 135, t_0 - 11]与[t_0 + 11, t_0 + 135]之并
        eva_nonevent_window_r = tmp_r_series.iloc[np.r_[tmp_loc-135:tmp_loc-10,tmp_loc+11:tmp_loc+136]]
        eva_nonevent_window_rf = r_f_data.loc[eva_nonevent_window_r.index]
        eva_nonevent_window_factors = factors_data.loc[eva_nonevent_window_r.index]
        eva_const = pd.DataFrame(1, index=eva_nonevent_window_r.index, columns=['const'])
        X = pd.concat([eva_const, eva_nonevent_window_rf, eva_nonevent_window_factors], axis=1).fillna(0).as_matrix()
        r_nonevent_hat = np.matmul(X, beta_hat) #据估计窗口所得risk loading计算非事件窗口日度收益fitted value
        ab_nonevent_r = np.transpose(eva_nonevent_window_r.fillna(0).as_matrix() - r_nonevent_hat) #非事件窗口日度abnormal return集
        
        #事件窗口: [t_0 - 1, t_0 + 1]
        eva_event_window_r = tmp_r_series.iloc[tmp_loc-1:tmp_loc+2]
        eva_event_window_rf = r_f_data.loc[eva_event_window_r.index]
        eva_event_window_factors = factors_data.loc[eva_event_window_r.index]
        eva_const = pd.DataFrame(1, index=eva_event_window_r.index, columns=['const'])
        X = pd.concat([eva_const, eva_event_window_rf, eva_event_window_factors], axis=1).fillna(0).as_matrix()
        r_event_hat = np.matmul(X, beta_hat) #据估计窗口所得risk loading计算事件窗口日度收益fitted value
        ab_event_r = np.transpose(eva_event_window_r.fillna(0).as_matrix() - r_event_hat) #事件窗口日度abnormal return集
        
        AIVol.iloc[e] = [np.std(ab_event_r,ddof=1)/np.std(ab_nonevent_r,ddof=1)-1,tmp_stock,tmp_fy] #两窗口日度abnormal return集的相对标准误
    except:
        continue
    
tmp_table = pd.pivot_table(AIVol, index=['Stock'], columns=['FY'], values='AIVol_[-1,1]', aggfunc=np.sum)
   
for e in range(len(event_sample)): 
    try:
        tmp_stock = event_sample.iloc[e]['股票代码']
        tmp_fy = event_sample.iloc[e]['会计年度']
        AIVol_est.iloc[e] = np.nanmean(
                tmp_table.loc[tmp_stock,tmp_table.columns[[tmp_table.columns.get_loc(tmp_fy)-2,tmp_table.columns.get_loc(tmp_fy)-1]]].values) #过往两年公告事件abnormal idiosyncratic volatility平均值作当前事件该变量的预期值
    except:
        continue
    
exceldata = AIVol_est
exceldata.to_excel('event_idiosyncratic_risk.xlsx')
