#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 21:39:33 2018

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

#导入非流动性指标数据
illiq_data_path = 'illiq_raw.xlsx'
illiq = pd.DataFrame(data=None)
illiq_xls = pd.ExcelFile(illiq_data_path)
for sheet in illiq_xls.sheet_names:
    tmp = pd.read_excel(illiq_xls,sheet)
    illiq = pd.concat([illiq,tmp], axis=0)   
illiq = pd.pivot_table(illiq,index=['Trddt'],columns=['Stkcd'],values='ILLIQ',aggfunc=np.nanmean)

illiq_re = pd.DataFrame(data=None, index=event_sample.index, columns=['ILLIQ'])

for e in range(len(event_sample)): #按事件样本作匹配
    try:
        tmp_event_date = pd.to_datetime(event_sample.iloc[e]['预计披露日期'])
        if tmp_event_date.isoweekday() == 6:
            tmp_event_date = (tmp_event_date + timedelta(days=2)).strftime('%Y-%m-%d')
        elif tmp_event_date.isoweekday() == 7:
            tmp_event_date = (tmp_event_date + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            tmp_event_date = (tmp_event_date).strftime('%Y-%m-%d')
        illiq_re.iloc[e]['ILLIQ'] = illiq.loc[tmp_event_date][event_sample.iloc[e]['股票代码']]
    except:
        continue
    
exceldata = illiq_re
exceldata.to_excel('event_illiquidity.xlsx')