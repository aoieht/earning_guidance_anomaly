#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 15:58:13 2018

@author: aoieht
"""

import pandas as pd
import numpy as np
from numpy.linalg import inv
from datetime import timedelta

event_path = '../raw_data/event_sample.xlsx'
abnormal_return_path = '../event_window_abnormal_return_three-factors/event_window_daily_abnormal_return.xlsx'
earning_forecast_path = '../event_earning_forecast_type/event_earning_forecast_type.xlsx'
earning_guidance_path = '../event_earning_guidance/earning_guidance_dummy.xlsx'
earning_surprise_path = '../event_earning_surprise/event_earning_surprise.xlsx'
idio_risk_path = '../event_idiosyncratic_risk/event_idiosyncratic_risk.xlsx'
illiq_path = '../event_illiquidity/event_illiquidity.xlsx'
industry_path = '../event_industry/event_industry.xlsx'
lnmv_path = '../event_market_value/event_market_capital.xlsx'
momentum_path = '../event_momentum/event_momentum.xlsx'
shortable_path = '../event_shortable/event_shortable.xlsx'
year_path = '../event_year/event_year.xlsx'

event_sample = pd.read_excel(event_path)
event_sample = event_sample.set_index(event_sample['股票代码'].map(str)+'@'+event_sample['会计年度'])
abnormal_return = pd.read_excel(abnormal_return_path)
idio_risk = pd.read_excel(idio_risk_path)
illiq = pd.read_excel(illiq_path)
earning_forecast_type = pd.read_excel(earning_forecast_path)
industry = pd.read_excel(industry_path)
year = pd.read_excel(year_path)
momentum = pd.read_excel(momentum_path)
lnmv = pd.read_excel(lnmv_path)
shortable = pd.read_excel(shortable_path)
earning_surprise = pd.read_excel(earning_surprise_path)
earning_guidance = pd.read_excel(earning_guidance_path)

reg_data = pd.DataFrame(data=None,index=event_sample.index)
reg_data = pd.concat([reg_data,
                      abnormal_return['CAR_[-5,-1]'],
                      earning_forecast_type,idio_risk,
                      illiq,momentum,
                      lnmv,
                      earning_surprise,
                      shortable,
                      earning_guidance,
                      year,industry],axis=1)

reg_data.to_excel('regression data.xlsx')