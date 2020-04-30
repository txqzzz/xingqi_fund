#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/18 2:14
# @Author  : Xingqi Tang
# @Contact : xingqitangatgmaildotcom
# @File    : go.py
# @Software: PyCharm
import ast
import re
from typing import List, Dict

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from docs import fund_info

fund_url_api = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
local_file_path = '/Users/dsay/2020/FUND_XINGQI/xingqi_fund'
current_worth_value_api = 'http://fundgz.1234567.com.cn/js/'


def get_url(url: str, params=None, proxies=None):
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text


def get_fund_data(code, per, sdate='', edate='', proxies=None):
    """
    :param edate: end_date
    :param sdate: start_date
    :param code: fund_code
    :param per: numbers of date_data per page
    :param proxies: proxies for scraping
    :rtype pd.dataFrame
    """
    params = {'type': 'lsjz', 'code': code, 'page': 1,
              'per': per, 'sdate': sdate, 'edate': edate}
    html = get_url(fund_url_api, params, proxies)
    soup = BeautifulSoup(html, 'html.parser')
    patt = re.compile(r'pages:(.*),')
    res = re.search(patt, html).group(1)
    pages = int(res)
    # record headers
    heads = []
    for head in soup.findAll("th"):
        heads.append(head.contents[0])
    # record
    records = []
    page = 1
    while page <= pages:
        params = {'type': 'lsjz', 'code': code, 'page': page,
                  'per': per, 'sdate': sdate, 'edate': edate}
        html = get_url(fund_url_api, params, proxies)
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')

        for row in soup.findAll('tbody')[0].findAll('tr'):
            row_records = []
            for record in row.findAll('td'):
                val = record.contents

                if not val:
                    row_records.append(np.nan)
                else:
                    row_records.append(val[0])
            records.append(row_records)
        page += 1
    # convert data into dataFrame
    np_records = np.array(records)
    fund_data = pd.DataFrame()
    for col, col_name in enumerate(heads):
        fund_data[col_name] = np_records[:, col]
    return fund_data


def get_cur_value(code: str, proxies=None):
    params = {'code': code}
    cur_url = current_worth_value_api + code + '.js'
    html = get_url(cur_url, params, proxies)
    patt = re.compile(r'jsonpgz\((.*)\)')
    res = re.search(patt, html).group(1)
    res_dict = ast.literal_eval(res)
    return res_dict


def list_current_fund_info(code: str):
    current_code: list[str] = get_cur_value(code)
    print('Current Code Fund Basic Information is listed as follows:\n',
          'fundCode:' + current_code['fundcode'] + '\n',
          'name:' + current_code['name'] + '\n',
          'date' + current_code['jzrq'] + '\n',
          'netAssetValue:' + current_code['dwjz'] + '\n',
          'netWorthValue:' + current_code['gsz'] + '\n',
          'dailyGrowthRate:' + current_code['gszzl'] + '\n',
          'time:' + current_code['gztime'])


def notification(code: str, buy: List[str] = None):
    assert isinstance(code, str)
    buyStock = buy
    data = get_fund_data(code, per=20, sdate='2020-01-01', edate='2020-12-31')
    data['净值日期'] = pd.to_datetime(data['净值日期'], format='%Y/%m/%d')
    data['单位净值'] = data['单位净值'].astype(float)
    data['累计净值'] = data['累计净值'].astype(float)
    data['日增长率'] = data['日增长率'].str.strip('%').astype(float)
    data = data.sort_values(by='净值日期', axis=0, ascending=True).reset_index(drop=True)
    ma20 = np.mean(data[-20:]['单位净值']).astype(float)
    # 90 trading days data
    df90 = data[-90:][1::]
    df90.to_csv(local_file_path + '/data/' + '%s' % code + '.csv')
    current_worth_value = float(get_cur_value(code)["gsz"])
    current_fund_name = get_cur_value(code)['name']
    try:
        if current_worth_value < ma20:
            buyStock.append(current_fund_name)
    except ValueError as e:
        assert current_worth_value
        print(e)


def daily_notification(buystock=None):
    buystock = []
    for code in fund_info.fund_id:
        notification(code, buystock)
    msg = 'Following Fund\'s current net value is lower than its MA20, please pay attention to them!\n' + str(buystock)
    msg_d = str(buystock)
    print(msg)
    return msg_d


def select_daily_ratio():
    # Identify all funds with a daily increase of more than 2.7% and decline of more than 2.5%
    increased_map: Dict[str, float] = {}
    decreased_map: Dict[str, float] = {}
    increased_params: float = 2.5
    decreased_params: float = -2.5
    for code in fund_info.fund_id:
        if float(get_cur_value(code)['gszzl']) >= increased_params:
            increased_map[str(get_cur_value(code)['name'])] = float(get_cur_value(code)['gszzl'])
        if float(get_cur_value(code)['gszzl']) <= decreased_params:
            decreased_map[str(get_cur_value(code)['name'])] = float(get_cur_value(code)['gszzl'])
    return increased_map, decreased_map


'''
select_i, select_d = select_daily_ratio()
sorted_select_i = sorted(select_i.items(), key=operator.itemgetter(1))
sorted_select_d = sorted(select_d.items(), key=operator.itemgetter(1), reverse=True)
print("Increased fund list:", sorted_select_i)
print("Decreased fund list:", sorted_select_d)
'''
