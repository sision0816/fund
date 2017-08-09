#!/usr/bin/evn python
# -*- coding:utf-8 -*-
############################################################################
'''
# 程序：东方财富网基金数据爬取
# 功能：抓取东方财富网上基金相关数据
# 创建时间：2017/02/14 基金概况数据
# 更新历史：2017/02/15 增加基金净值数据
#
# 使用库：requests、BeautifulSoup4、pymysql,pandas
# 作者：yuzhucu
'''
#############################################################################
import requests
from bs4 import BeautifulSoup
import time
import random
import pymysql
import os
import pandas as pd
import re


def getCurrentTime():
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

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

class FundAnalysis():

    def getCurrentTime(self):
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def getFundCodesFromCsv(self):
        '''
        从csv文件中获取基金代码清单（可从wind或者其他财经网站导出）
        '''
        file_path=os.path.join(os.getcwd(),'fund.csv')
        fund_code = pd.read_csv(filepath_or_buffer=file_path, encoding='gbk')
        Code=fund_code.trade_code
        #print ( Code)
        return Code

    def getFundInfo(self,fund_code):
        '''
        获取基金概况基本信息
        :param fund_code:
        :return:
        '''
        table = 'fund_info'
        my_key = ['fund_code', 'funder']
        cols = ', '.join([str(i) for i in my_key])
        sql = "select %s  from %s" % (cols, table)
        try:
            result = mySQL.fetchData(sql)
            print(result)
            print (self.getCurrentTime(),'Fund Info Insert Sucess:', result['fund_code'],result['fund_name'],result['fund_abbr_name'],result['fund_manager'],result['funder'],result['establish_date'],result['establish_scale'],result['benchmark'] )
        except  Exception as e:
            print (self.getCurrentTime(), e )


        return result

    def getFundManagers(self,fund_code):
        '''
        获取基金经理数据。 基金投资分析关键在投资经理，后续在完善
        :param fund_code:
        :return:
        '''
        fund_url='http://fund.eastmoney.com/f10/jjjl_'+str(fund_code) +'.html'
        res = getURL(fund_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = {}
        manager={}
        tables=soup.find_all("table")
        tab = tables[1]
        #print (tables[1])
        i=0
        #先用本办法，解析表格，逐行逐单元格获取净值数据
        for tr in tab.findAll('tr'):
            #跳过表头；获取净值、累计净值和日收益率数据 如果列数为7，可以判断为一般基金。当然也可以通过标题或者基金类型参数来判断，待后续优化
            if tr.findAll('td') :#and len((tr.findAll('td')))==7 :
                i=i+1
                try:
                     result['fund_code']=fund_code
                     result['start_date']= tr.select('td:nth-of-type(1)')[0].getText().strip()
                     result['end_date']= tr.select('td:nth-of-type(2)')[0].getText().strip()
                     result['fund_managers']= tr.select('td:nth-of-type(3)')[0].getText().strip()
                     result['term']= tr.select('td:nth-of-type(4)')[0].getText().strip()
                     result['return_rate']= tr.select('td:nth-of-type(5)')[0].getText().strip('%')+'%'
                     result['created_date']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                     result['updated_date']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                     result['data_source']='eastmoney'

                except  Exception as e:
                     print (self.getCurrentTime(),'getFundManagers1', fund_code,fund_url,e )

                try:
                    mySQL.insertData('fund_managers_chg', result)
                    print (self.getCurrentTime(),'fund_managers_chg:',result['fund_code'],i,result['start_date'],result['end_date'],result['fund_managers'],result['term'],result['return_rate'] )
                except  Exception as e:
                    print (self.getCurrentTime(),'getFundManagers2', fund_code,fund_url,e )

                for a in tr.findAll('a'):
                    if a:
                        try:
                            manager['manager_id']=a['href'].strip('http://fund.eastmoney.com/manager/.html')
                            manager['url']=a['href']
                            manager['manager_name']=a.text
                            manager['created_date']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                            manager['updated_date']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                            manager['data_source']='eastmoney'
                            #print (self.getCurrentTime(),manager['manager_id'],manager['manager_name'],manager['url'])
                        except Exception as e:
                            print (self.getCurrentTime(),'getFundManagers3', fund_code,manager['manager_name'],manager['url'],fund_url,e )

                        try:
                            mySQL.insertData('fund_managers_info', manager)
                            print (self.getCurrentTime(),'fund_managers_info:',fund_code,manager['manager_name'],manager['url'],manager['manager_id'] )
                        except  Exception as e:
                            print (self.getCurrentTime(),'getFundManagers4', fund_code,fund_url,e )
        #print (self.getCurrentTime(),'getFundManagers',result['fund_code'],'共',str(i)+':','行数保存成功'   )

        return result

    def getFundNav(self,fund_code):
        '''
        获取基金净值数据，因为基金列表中是所有基金代码，一般净值型基金和货币基金数据稍有差异，下面根据数据表格长度判断是一般基金还是货币基金，分别入库
        :param fund_code:
        :return:
        '''
        try:
             #http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=000001&page=1&per=1
             '''
             #寿险获取单个基金的第一页数据，里面返回的apidata 接口中包含了记录数、分页及数据文件等
             #这里暂按照字符串解析方式获取，既然是标准API接口，应该可以通过更高效的方式批量获取全部净值数据，待后续研究。这里传入基金代码、分页页码和每页的记录数。先简单查询一次获取总的记录数，再一次性获取所有历史净值
             首次初始化完成后，如果后续每天更新或者定期更新，只要修改下每页返回的记录参数即可
            '''
             fund_url='http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code='+str(fund_code) +'&page=1&per=1'
             res = getURL(fund_url)
             #获取历史净值的总记录数
             records= (res.text.strip('var apidata=').strip('{;}').split(',')[1].strip('records:'))
             #print(res.text.strip('var apidata=').strip('{;}').split(','))
             #print (records)
        except  Exception as e:
            print (self.getCurrentTime(),'getFundNav1', fund_code,fund_url,e )
        try:
            #根据基金代码和总记录数，一次返回所有历史净值
            fund_nav='http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code='+str(fund_code) +'&page=1&per='+records
            res = getURL(fund_nav)
            soup = BeautifulSoup(res.text, 'html.parser')
        except  Exception as e:
            print (self.getCurrentTime(),'getFundNav2', fund_code,fund_url,e )

        result={}
        result['fund_code']=fund_code
        tables = soup.findAll('table')
        tab = tables[0]
        i=0
        #先用本办法，解析表格，逐行逐单元格获取净值数据
        for tr in tab.findAll('tr'):
            #跳过表头；获取净值、累计净值和日收益率数据 如果列数为7，可以判断为一般基金。当然也可以通过标题或者基金类型参数来判断，待后续优化
            if tr.findAll('td') and len((tr.findAll('td')))==7 :
                i=i+1
                try:
                     result['the_date']= (tr.select('td:nth-of-type(1)')[0].getText().strip() )
                     result['nav']= (tr.select('td:nth-of-type(2)')[0].getText().strip() )
                     result['add_nav']= (tr.select('td:nth-of-type(3)')[0].getText().strip() )
                     result['nav_chg_rate']= (tr.select('td:nth-of-type(4)')[0].getText().strip() )
                     result['buy_state']= (tr.select('td:nth-of-type(5)')[0].getText().strip() )
                     result['sell_state']= tr.select('td:nth-of-type(6)')[0].getText().strip()
                     result['div_record']= tr.select('td:nth-of-type(7)')[0].getText().strip().strip('\'')
                     #print (self.getCurrentTime(),i,result['fund_code'],result['the_date'],result['nav'],result['add_nav'],result['nav_chg_rate'],result['buy_state'],result['sell_state'] )
                except  Exception as e:
                     print (self.getCurrentTime(),'getFundNav3', fund_code,fund_url,e )
                try:
                    mySQL.insertData('fund_nav', result)
                    print (self.getCurrentTime(),'fund_nav',str(i)+'/'+str(records),result['fund_code'],result['the_date'],result['nav'],result['add_nav'],result['nav_chg_rate'],result['buy_state'],result['sell_state'],result['div_record'] )
                except  Exception as e:
                    print (self.getCurrentTime(),'getFundNav4', fund_code,fund_url,e )
            #如果是货币基金，获取万份收益和7日年化利率
            elif  tr.findAll('td') and len((tr.findAll('td')))==6:
                i=i+1
                try:
                     result['the_date']= (tr.select('td:nth-of-type(1)')[0].getText().strip() )
                     #result['nav']=1
                     result['profit_per_units']= (tr.select('td:nth-of-type(2)')[0].getText().strip() )
                     result['profit_rate']= (tr.select('td:nth-of-type(3)')[0].getText().strip() )
                     result['buy_state']= (tr.select('td:nth-of-type(4)')[0].getText().strip() )
                     result['sell_state']= (tr.select('td:nth-of-type(5)')[0].getText().strip() )
                     result['div_record']= (tr.select('td:nth-of-type(6)')[0].getText().strip() )
                     #print (self.getCurrentTime(),i,result['fund_code'],result['the_date'],result['nav'],result['add_nav'],result['nav_chg_rate'],result['buy_state'],result['sell_state'] )
                except  Exception as e:
                     print (self.getCurrentTime(),'getFundNav5', fund_code,fund_url,e )
                try:
                    mySQL.insertData('fund_nav_currency', result)
                    print (self.getCurrentTime(),'fund_nav_currency',str(i)+'/'+str(records),result['fund_code'],result['the_date'],result['profit_per_units'],result['profit_rate'],result['buy_state'],result['sell_state'] )
                except  Exception as e:
                    print (self.getCurrentTime(),'getFundNav6', fund_code,fund_url,e )
            else :
                pass
            # if i>=1:
            #     break
        print (self.getCurrentTime(),'getFundNav',result['fund_code'],'共',str(i)+'/'+str(records),'行数保存成功'   )

        return result




def main():
    global mySQL, sleep_time, isproxy, proxy, header
    mySQL = PyMySQL()
    fundAnalysis=FundAnalysis()
    mySQL._init_('localhost', 'root', 'wangxing', 'fund')
    isproxy = 0  # 如需要使用代理，改为1，并设置代理IP参数 proxy
    proxy = {"http": "http://110.37.84.147:8080", "https": "http://110.37.84.147:8080"}#这里需要替换成可用的代理IP
    sleep_time = 0.1
    #fundAnalysis.getFundJbgk('000001')
    funds=fundAnalysis.getFundCodesFromCsv()
    #fundAnalysis.getFundManagers('000001')
    for fund in funds:
         try:
             fundAnalysis.getFundInfo(fund)
             # fundAnalysis.getFundManagers(fund)
             # fundAnalysis.getFundNav(fund)
         except Exception as e:
            print (getCurrentTime(),'main', fund,e )

if __name__ == "__main__":
    main()
