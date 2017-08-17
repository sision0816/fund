# -*- coding:utf-8 -*-
############################################################################
'''
# 功能：抓取东方财富网上基金相关数据
# 使用库：requests、BeautifulSoup4、pymysql,pandas
# 作者：Xing Wang
'''
############################################################################
from fund.database.fundspiders import FundSpiders, randHeader
from fund.database.fundmysql import PyMySQL
from datetime import date
import pandas as pd

mySQL = PyMySQL('localhost', 'root', 'wangxing', 'fund')
fundSpiders=FundSpiders(mySQL)

# funds=fundSpiders.getFundCodesFromCsv('fundlist.csv')
funds=fundSpiders.getFundCodesFromCsv('myfund.csv')
for fund in funds:
     try:
         # fundSpiders.getFundInfo(fund)
         # fundSpiders.getFundManagers(fund)
         fundSpiders.getFundNav(fund, update = True)
     except Exception as e:
        print (getCurrentTime(),'main', fund,e )