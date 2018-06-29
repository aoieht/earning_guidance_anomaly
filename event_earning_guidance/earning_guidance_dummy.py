
import pandas as pd
import numpy as np
from numpy.linalg import inv
from datetime import timedelta

event_path = '../raw_data/event_sample.xlsx'
earning_guidance_path = ['../raw_data/historical_earning_guidance/业绩快报2010.xlsx','../raw_data/historical_earning_guidance/业绩快报2011-2016.xlsx']

event_sample = pd.read_excel(event_path)
event_sample = event_sample.set_index(event_sample['股票代码'].map(str)+'@'+event_sample['会计年度'])
earning_guidance_data = None
for xls in earning_guidance_path:
    tmp = pd.read_excel(xls,'report_date')
    earning_guidance_data = pd.concat([earning_guidance_data,tmp],axis=0)

earning_guidance = pd.pivot_table(earning_guidance_data,index='证券代码',columns='FY',values='业绩快报披露日',aggfunc='first')

earning_guidance_re = pd.DataFrame(data=None,index=event_sample.index,columns=['Earning Guidance'])

for e in range(len(event_sample)):
    tmp_stock = event_sample.iloc[e]['股票代码']
    tmp_FY = pd.to_datetime(event_sample.iloc[e]['会计年度'])
    try:
        if earning_guidance.loc[tmp_stock,tmp_FY] is pd.NaT:
            earning_guidance_re.iloc[e]['Earning Guidance'] = 0
        else:
            earning_guidance_re.iloc[e]['Earning Guidance'] = 1
    except:        
        continue

exceldata = earning_guidance_re.fillna(0)
exceldata.to_excel('earning_guidance_dummy.xlsx')