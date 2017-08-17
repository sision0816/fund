#!/usr/bin/python3
# -*- coding:utf8 -*-
############################################################################
'''
# 功能：抓取东方财富网上基金相关数据
# 使用库：requests、BeautifulSoup4、pymysql,pandas
# 作者：Xing Wang
'''
############################################################################
from fundmysql import PyMySQL
from pyfund import Fund
from datetime import date
import pandas as pd

#
mySQL = PyMySQL('localhost', 'root', 'wangxing', 'fund')
fund_codes = pd.read_csv(filepath_or_buffer='fund_c.csv', sep = '\s+', dtype=str, encoding='utf8').trade_code
# fund_codes = pd.read_csv(filepath_or_buffer='myfund.csv', sep = '\s+', dtype=str, encoding='utf8').trade_code

myfundcode = []
today = date.today()
print(today)
for fund_code in fund_codes:
	print(fund_code)
	myfund=Fund(mySQL = mySQL, fund_code = fund_code)
	myfund.getFundInfo()
	myfund.getFundNav()
	# myfund.printFundInfo()
	try:
		rets = [myfund.calcRet(mode = 'week'),myfund.calcRet(mode = 'month')] 
	except Exception as e:
		print('error: ', fund_code, e)
	print('week     month')
	print('{0:1.2f}%    {1:1.2f}%'.format(rets[0]*100, rets[1]*100))
	if rets[0]<-0.01 and rets[1]>0.04:
		myfund.printFundInfo()
		myfundcode.append(fund_code)

print(myfundcode)
