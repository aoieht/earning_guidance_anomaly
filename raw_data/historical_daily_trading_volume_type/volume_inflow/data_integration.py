#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 21:28:47 2018

@author: aoieht
"""

import pandas as pd

tmp_types = ['B','I','M','S']
names = locals()
for ttype in tmp_types:
    names['volume_inflow_'+ttype] = None
for tyear in range(2012,2017):
    for ttype in tmp_types:
        tmp_path = str(tyear)+ttype+'.xlsx'
        tmp_data = pd.read_excel(tmp_path,index_col=0,header=3)
        names['volume_inflow_'+ttype] = pd.concat([names['volume_inflow_'+ttype],tmp_data],axis=0)
        
excelwriter = pd.ExcelWriter('volume_inflow.xlsx')
for ttype in tmp_types:
    names['volume_inflow_'+ttype].to_excel(excelwriter,'volume_inflow_'+ttype)
excelwriter.save()