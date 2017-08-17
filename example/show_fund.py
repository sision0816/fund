# -*- coding:utf-8 -*-
############################################################################
'''
# 功能：抓取东方财富网上基金相关数据
# 使用库：requests、BeautifulSoup4、pymysql,pandas
# 作者：Xing Wang
'''
############################################################################
from 	database.fundmysql import PyMySQL
from pyfund.pyfund import Fund
import pandas as pd

mySQL = PyMySQL('localhost', 'root', 'wangxing', 'fund')
fund_codes = pd.read_csv(filepath_or_buffer='myfund.csv', sep = '\s+', dtype=str, encoding='utf8').trade_code
for fund_code in fund_codes:
	myfund=Fund(mySQL = mySQL, fund_code = fund_code)
	myfund.getFundInfo()
	myfund.getFundNav()
	myfund.printFundInfo()
	myfund.plotNav()
	rets = [myfund.calcRet(mode = 'week'),myfund.calcRet(mode = 'month')] 
	print('week     month')
	print('{0:1.2f}%    {1:1.2f}%'.format(rets[0]*100, rets[1]*100))
	# ret = myfund.BuySell()
	# print(ret)
	# myfund.plotNav()
	# myfund.plotStrategy()