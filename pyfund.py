# -*- coding:utf-8 -*-
############################################################################
'''
#Author: Xing Wang
'''
#############################################################################
import time
import random
import pymysql
import os
import pandas as pd
import re
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange


class PyMySQL:
    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    # 数据库初始化
    def _init_(self, host, user, passwd, db,port=3306,charset='utf8'):
        pymysql.install_as_MySQLdb()
        try:
            self.db =pymysql.connect(host=host,user=user,passwd=passwd,db=db,port=3306,charset='utf8')
            self.db.ping(True)#使用mysql ping来检查连接,实现超时自动重新连接
#            print (self.getCurrentTime(), u"MySQL DB Connect Success:",user+'@'+host+':'+str(port)+'/'+db)
            self.cur = self.db.cursor()
            self.cur_dict = self.db.cursor(pymysql.cursors.DictCursor)
        except  Exception as e:
            print (self.getCurrentTime(), u"MySQL DB Connect Error :%d: %s" % (e.args[0], e.args[1]))
    # fetch
    def fetchData(self, sql):
        # print(table)
#        print(sql)
        try:
            self.cur_dict.execute(sql)
            results = self.cur_dict.fetchall()
        except Exception as e:
            # 发生错误时回滚
            print (self.getCurrentTime(), u"Data Fetch Failed: %s" % (e))
        return results

class Manager():
    '''
    '''
    def __init__(self, manager_id = None):
        self. manager_id = manager_id      # '基金代码',
        self.info = {
                        'manager_id'    : '基金代码',
                        'url'           : '基金全称',
                        'manager_name'  : '基金简称',
                        'created_date'  : '基金类型',
                        'updated_date'  : '发行日期',
                        'data_source'   : '成立日期',
                        }
    def getManagerInfo(self, ):
        pass

class Fund():
    '''
    '''
    def __init__(self, fund_code =None, fund_abbr_name =None, **kwargs):
        self.fund_code = fund_code # 基金代码',
        self.info      = None
        self.nav       = None
        self.info_dict = {
                        'fund_name'          : '基金全称',
                        'fund_abbr_name'     : '基金简称',
                        'fund_type'          : '基金类型',
                        'issue_date'         : '发行日期',
                        'establish_date'     : '成立日期',
                        'establish_scale'    : '成立日期规模',
                        'asset_value'        : '最新资产规模',
                        'asset_value_date'   : '最新资产规模日期',
                        'units'              : '最新份额规模',
                        'units_date'         : '最新份额规模',
                        'fund_manager'       : '基金管理人',
                        'fund_trustee'       : '基金托管人',
                        'funder'             : '基金经理人',
                        'total_div'          : '成立来分红',
                        'mgt_fee'            : '管理费率',
                        'trust_fee'          : '托管费率',
                        'sale_fee'           : '销售服务费率',
                        'buy_fee'            : '最高认购费率',
                        'buy_fee2'           : '最高申购费率',
                        'benchmark'          : '业绩比较基准',
                        'underlying'         : '跟踪标的',
                        'data_source'        : '数据来源',
                        'created_date'       : '创建时间',
                        'updated_date'       : '更新时间',
                        'created_by'         : '创建人',
                        'updated_by'         : '更新人',
                        }
        self.nav_dict = {         
                        'the_date'         : '净值日期',
                        'nav'              : '单位净值',
                        'add_nav'          : '累计净值',
                        'nav_chg_rate'     : '日增长率',
                        'buy_state'        : '申购状态',
                        'sell_state'       : '赎回状态',
                        'div_record'       : '分红送配',
                        'created_date'     : '创建时间',
                        'updated_date'     : '更新时间',
                        }

        self.set(**kwargs)

    def set(self, **kwargs):
            pass

    def getFundInfo(self):
        '''
        读取基金信息
        '''
        table = 'fund_info'
#        my_key = ['fund_abbr_name', 'nav', 'add_nav', 'nav_chg_rate']
#        cols = ','.join([str(i) for i in my_key])
        sql = "select *  from %s where fund_code = %s" % (table, self.fund_code)
        try:
#            self.info = mySQL.fetchData(sql)
            self.info = pd.read_sql(sql, con = mySQL.db, index_col='fund_code')
#            print(self.info)
        except  Exception as e:
            print(e)
    def getFundNav(self):
        '''
        读取历史净值
        '''
        table = 'fund_nav'
        my_key = ['the_date', 'nav', 'add_nav', 'nav_chg_rate', 'buy_state', 'sell_state']
        cols = ','.join([str(i) for i in my_key])
        sql = "select %s  from %s where fund_code = %s" % (cols, table, self.fund_code)
        # sql = "select *  from %s where fund_code = %s" % (table, self.fund_code)
        try:
            self.nav = pd.read_sql(sql, con = mySQL.db, index_col='the_date')
            self.nav.index = self.nav.index.str.strip()
            self.nav[:] = self.nav[:].str.strip()
            # self.nav = self.nav[-1::]
        except  Exception as e:
            print(e)
    def BuySell(self, ):
        #
        buy = []
        sell = []
        totalRet = 0
        n = len(self.nav)
        i = 0
        n1 = 5
        n2 = 1
        while i < n - n1:
            hisret1 = self.calcRet(self.nav.index[i - 1], self.nav.index[i])
            hisret2 = self.calcRet(self.nav.index[i - n1], self.nav.index[i])
            print(self.nav.index[i], hisret1, hisret2)
            # 买入新的股票
            if (hisret1 < -0.01):
                buydate = self.nav.index[i]
                while i < n - n1:
                    i += 1
                    hisret = self.calcRet(self.nav.index[i - n2], self.nav.index[i])
                    if hisret<-0.005:
                        selldate = self.nav.index[i]
                        break
                myret = self.calcRet(buydate, selldate) - 0.005
                print('***', buydate, selldate, myret)
                buy.append({'the_date': buydate, 'nav': self.nav.loc[buydate]['nav']})
                sell.append({'the_date': selldate, 'nav': self.nav.loc[selldate]['nav']})
                totalRet += myret
            else:
                i += 1
        print('Total: ', totalRet)
        self.buy = pd.DataFrame(buy)
        self.buy.set_index('the_date', inplace = True)
        self.sell = pd.DataFrame(sell)
        self.sell.set_index('the_date', inplace = True)
        print(self.buy)
        print(self.sell)
        return totalRet;
    def calcRet(self, begin, end):
        # calc the return
        ret = (self.nav.loc[end]['nav'] - self.nav.loc[begin]['nav'])/self.nav.loc[begin]['nav']
        return ret

    def printFundInfo(self,):
        print('\n')
        print('----------------------------------')
        print(u'基金代码:    %s'%(self.fund_code))
        print(u'基金简称:    %s'%(self.info.iloc[0]['fund_abbr_name']))
        print(u'基金类型:    %s'%(self.info.iloc[0]['fund_type']))
        print(u'发行日期:    %s'%(self.info.iloc[0]['issue_date']))
        print(u'基金经理人:  %s'%(self.info.iloc[0]['funder']))
        #输出历史净值
        print('\n\n')
        print('-----------------------------------------------------------')
        print('净值日期    单位净值    累计净值    日增长率    申购状态    赎回状态')
        print(self.nav.tail(5))
        print('-----------------------------------------------------------')
        print('\n\n')
        # self.printNav(5)
    def plotNav(self, ):
        import datetime
        from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
        fig, ax = plt.subplots()
        ax.plot_date(self.nav.index, self.nav['nav'], '-')
        ax.set_xlim(pd.Timestamp(self.nav.index[0]), pd.Timestamp(self.nav.index[-1]))
        ax.plot_date(self.buy.index, self.buy['nav'], 'rs')
        plt.show()
        return 0    
    def plotStrategy(self, ):
        fig, ax = plt.subplots()
        ax.plot_date(self.nav.index, self.nav['nav'], '-')
        ax.set_xlim(pd.Timestamp(self.nav.index[0]), pd.Timestamp(self.nav.index[100]))
        ax.plot_date(self.buy.index, self.buy['nav'], 'gs')
        ax.plot_date(self.sell.index, self.sell['nav'], 'rs')
        plt.show()
        return 0  

    def printNav(self, ndays):
        # Define the new names of your columns
        print('净值日期    单位净值    累计净值    日增长率    申购状态    赎回状态')
        for i in range(-5, -1, 1):
            text = ''.join([self.nav.index[i]])
            for j in range(5):
                text += '    ' + str(self.nav.iloc[i][j])
            print(text)




def main():
    global mySQL
    mySQL = PyMySQL()
    mySQL._init_('localhost', 'root', 'wangxing', 'fund')
    myfund=Fund(fund_code = '000001')
    myfund.getFundInfo()
    myfund.getFundNav()
    myfund.printFundInfo()
    print(myfund.calcRet('2016-12-29', '2017-08-09'))
    # ret = myfund.BuySell()
    # print(ret)
    # myfund.plotNav()
    # myfund.plotStrategy()



if __name__ == "__main__":
    main()
