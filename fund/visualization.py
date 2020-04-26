#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 15:10
# @Author  : Xingqi Tang
# @Contact : xingqitangatgmaildotcom
# @File    : visualization.py
# @Software: PyCharm
import matplotlib.pyplot as plt
import fund.fund_utils as fut

fig = plt.figure()
code = '000068'  # todo: here to make an example, make it flexible later
data = fut.get_fund_data(code, per=20, sdate='2020-01-01', edate='2020-12-31')
net_value_date = data['净值日期']
net_asset_value = data['单位净值']
accumulative_net_value = data['累计净值']
daily_growth_rate = data['日增长率']
ax1 = fig.add_subplot(111)
ax1.plot(net_value_date, net_asset_value)
ax1.plot(net_value_date, accumulative_net_value)
ax1.set_ylabel('netValue')
ax1.set_xlabel('Date')
plt.legend(loc='upper left')

ax2 = ax1.twinx()
ax1.plot(net_value_date, daily_growth_rate, 'r')
ax1.set_ylabel('dailyGrowthRate')
plt.legend(loc='upper right')

plt.show()
