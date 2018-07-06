import pandas as pd
import numpy as np
from datetime import timedelta

if __name__ == '__main__':

    # 导入事件样本
    event_path = '../raw_data/event_sample.xlsx'
    event_sample = pd.read_excel(event_path)
    event_sample = event_sample.set_index(event_sample['股票代码'].map(str) + '@' + event_sample['会计年度'])

    daily_volume_path = '../raw_data/historical_daily_trading_volume_all_stock/daily_trading_volume.xlsx'
    volume_inflow_path = '../raw_data/historical_daily_trading_volume_type/volume_inflow/volume_inflow.xlsx'
    volume_outflow_path = '../raw_data/historical_daily_trading_volume_type/volume_outflow/volume_outflow.xlsx'

    volume = pd.read_excel(daily_volume_path)
    volume = volume.set_index(pd.to_datetime(volume['Trddt']))

    tmp_types = ['B', 'I', 'M', 'S']
    names = locals()
    for ttype in tmp_types:
        names['volume_inflow_' + ttype] = pd.read_excel(volume_inflow_path, 'volume_inflow_' + ttype).set_index('Date')
        names['volume_outflow_' + ttype] = pd.read_excel(volume_outflow_path, 'volume_outflow_' + ttype).set_index(
            'Date')

    tmp_columns = []
    for i in range(-10, 11):  # 事件窗口列标签
        tmp_columns.append('t_' + str(i))

    excelwriter = pd.ExcelWriter('net_inflow.xlsx')

    for ttype in tmp_types:
        names['net_inflow_' + ttype] = pd.DataFrame(data=None, index=event_sample.index, columns=tmp_columns)
        for e in range(len(event_sample)):
            try:
                tmp_stock = event_sample.iloc[e]['股票代码']
                if tmp_stock < 600000:
                    tmp_stock_re = "{0:0>6}".format(tmp_stock) + '.SZ'
                else:
                    tmp_stock_re = "{0:0>6}".format(tmp_stock) + '.SH'

                tmp_event_date = pd.to_datetime(event_sample.iloc[e]['预计披露日期'])
                if tmp_event_date.isoweekday() == 6:  # 公告日为周末的调整为交易日
                    tmp_event_date = (tmp_event_date + timedelta(days=2))
                elif tmp_event_date.isoweekday() == 7:
                    tmp_event_date = (tmp_event_date + timedelta(days=1))
                else:
                    tmp_event_date = tmp_event_date

                tmp_volume_series = volume.loc[:, tmp_stock].dropna()
                tmp_inflow_series = names['volume_inflow_' + ttype].loc[:, tmp_stock_re].dropna()
                tmp_outflow_series = names['volume_outflow_' + ttype].loc[:, tmp_stock_re].dropna()
                tmp_loc = tmp_volume_series.index.get_loc(tmp_event_date)
                eva_window_volume = tmp_volume_series.iloc[tmp_loc - 10:tmp_loc + 11]
                names['net_inflow_' + ttype].at[event_sample.index[e]] = np.divide(
                    (tmp_inflow_series.loc[eva_window_volume.index] -
                     tmp_outflow_series.loc[eva_window_volume.index]).values,
                    eva_window_volume.values * 10000)

            except:
                continue

        names['net_inflow_' + ttype].to_excel(excelwriter, 'net_inflow_' + ttype)

    excelwriter.save()
