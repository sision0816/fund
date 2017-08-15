# -*- coding:utf-8 -*-
############################################################################
'''
# 功能：抓取东方财富网上基金相关数据
# 使用库：requests、BeautifulSoup4、pymysql,pandas
# 作者：Xing Wang
'''
############################################################################
from fundspiders import PyMySQL, FundSpiders, randHeader

mySQL = PyMySQL()
fundSpiders=FundSpiders(mySQL)
mySQL._init_('localhost', 'root', 'wangxing', 'fund')
#fundSpiders.getFundJbgk('000001')
funds=fundSpiders.getFundCodesFromCsv('myfund.csv')
#fundSpiders.getFundManagers('000001')
for fund in funds:
     try:
         # fundSpiders.getFundInfo(fund)
         # fundSpiders.getFundManagers(fund)
         fundSpiders.getFundNav(fund, update = True)
     except Exception as e:
        print (getCurrentTime(),'main', fund,e )