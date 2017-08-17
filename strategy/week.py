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


class PyMySQL:
    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    # 数据库初始化
    def _init_(self, host, user, passwd, db,port=3306,charset='utf8'):
        pymysql.install_as_MySQLdb()
        try:
            self.db =pymysql.connect(host=host,user=user,passwd=passwd,db=db,port=3306,charset='utf8')
            #self.db = pymysql.connect(ip, username, pwd, schema,port)
            self.db.ping(True)#使用mysql ping来检查连接,实现超时自动重新连接
            print (self.getCurrentTime(), u"MySQL DB Connect Success:",user+'@'+host+':'+str(port)+'/'+db)
            self.cur = self.db.cursor()
        except  Exception as e:
            print (self.getCurrentTime(), u"MySQL DB Connect Error :%d: %s" % (e.args[0], e.args[1]))
    # fetch
    def fetchData(self, sql):
        # print(table)
        print(sql)
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
        except Exception as e:
            # 发生错误时回滚
            print (self.getCurrentTime(), u"Data Fetch Failed: %s" % (e))
        return results

class Week():

    def getCurrentTime(self):
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def getFundCodesFromCsv(self, filename = 'fund.csv'):
        '''
        从csv文件中获取基金代码清单（可从wind或者其他财经网站导出）
        '''
        file_path=os.path.join(os.getcwd(),'fund.csv')
        fund_code = pd.read_csv(filepath_or_buffer=file_path, encoding='gbk')
        Code=fund_code.trade_code
        #print ( Code)
        return Code


    def getFundNav(self,fund_code):
        '''
        获取基金概况基本信息
        :param fund_code:
        :return:
        '''

        table = 'fund_nav'
        my_key = ['the_date', 'nav', 'nav_chg_rate']
        cols = ', '.join([str(i) for i in my_key])
        sql = "select %s  from %s where fund_code = %s" % (cols, table, fund_code)
        try:
            datas = mySQL.fetchData(sql)
            # print(datas)
            for data in datas:
                print(data)
            # print (self.getCurrentTime(),'Fund Nav Fetch Sucess:', datas[:, 0], datas[:, 1])
        except  Exception as e:
            print (self.getCurrentTime(), e )
        navs = []
        rates = []
        for data in datas:
            # print(data)
            nav = data[1]
            rate = data[2].split('%')[0].strip()
            if rate:
                print(rate)
                navs.append(nav)
                rates.append(float(rate))
        self.navs = navs
        self.rates = rates
        for i in range(len(self.rates)):
            print(i, self.rates[i])
    #
    def plotNav(self, ):
        plt.plot(self.navs)
        dates = []
        values = []
        for date in self.invs:
            dates.append(date[0])
            values.append(self.navs[date[0]])
        plt.plot(dates, values, 's')
        plt.show()
        return 0
    #
    def BuySell(self, ):
        #
        totalRet = 0
        n = len(self.rates)
        i = 20
        n1 = 2
        n2 = 3
        invs = []
        while i < n - n1:
            weeknav = self.calcWeekNav(i, n1)
            print(i, weeknav)

        # 买入新的股票
            if (weeknav < -1.0):
                buydate = i
                while i < n - n1:
                    i += 1
                    weeknav = self.calcWeekNav(i, 1)
                    if weeknav<-1.0:
                        break
                myret = self.calcReturn(buydate, i - buydate) - 0.5
                print(i, myret)
                invs.append([buydate, myret])
                totalRet += myret
            else:
                i += 1
        print('Total: ', totalRet)
        self.invs = invs
        return totalRet;

    def calcWeekNav(self, date, ndays):
        #
        weeknav = 0
        for i in range(date - ndays, date + 1):
            weeknav += float(self.rates[i])

        return weeknav
    def calcReturn(self, begin, end):
        #
        myret = 0
        for i in range(date + 1, date + ndays):
            myret = myret + self.rates[i]
        return myret
def main():
    global mySQL
    mySQL = PyMySQL()
    week=Week()
    mySQL._init_('localhost', 'root', 'wangxing', 'fund')
    proxy = {"http": "http://110.37.84.147:8080", "https": "http://110.37.84.147:8080"}#这里需要替换成可用的代理IP
    sleep_time = 0.1
    funds=week.getFundCodesFromCsv('fund.csv')
    for fund in funds:
        navs=week.getFundNav(fund)
        myret=week.BuySell()
        week.plotNav()


if __name__ == "__main__":
    main()
