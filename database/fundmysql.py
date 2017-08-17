# -*- coding:utf-8 -*-
############################################################################
'''
# 功能：抓取东方财富网上基金相关数据
# 使用库：requests、BeautifulSoup4、pymysql,pandas
# 作者：Xing Wang
'''
#############################################################################
import time
import random
import pymysql
import os
import pandas as pd
import re


class PyMySQL:
    '''
    '''
    # 数据库初始化
    def __init__(self, host, user, passwd, db,port=3306,charset='utf8'):
        pymysql.install_as_MySQLdb()
        try:
            self.db =pymysql.connect(host=host,user=user,passwd=passwd,db=db,port=3306,charset='utf8')
            #self.db = pymysql.connect(ip, username, pwd, schema,port)
            self.db.ping(True)#使用mysql ping来检查连接,实现超时自动重新连接
            print (self.getCurrentTime(), u"MySQL DB Connect Success:",user+'@'+host+':'+str(port)+'/'+db)
            self.cur = self.db.cursor()
        except  Exception as e:
            print (self.getCurrentTime(), u"MySQL DB Connect Error :%d: %s" % (e.args[0], e.args[1]))
    # 插入数据
    def insertData(self, table, my_dict):
        # print(table)
        # print(my_dict)
        try:
            #self.db.set_character_set('utf8')
            cols = ','.join(my_dict.keys())
            values = '","'.join([str(i) for i in my_dict.values()])
            sql = "replace into %s (%s) values (%s)" % (table, cols, '"' + values + '"')
            #print (sql)
            try:
                result = self.cur.execute(sql)
                insert_id = self.db.insert_id()
                self.db.commit()
                # 判断是否执行成功
                if result:
                    #print (self.getCurrentTime(), u"Data Insert Sucess")
                    return insert_id
                else:
                    return 0
            except Exception as e:
                # 发生错误时回滚
                self.db.rollback()
                print (self.getCurrentTime(), u"Data Insert Failed: %s" % (e))
                return 0
        except Exception as e:
            print (self.getCurrentTime(), u"MySQLdb Error: %s" % (e))
            return 0
        # Check data exist
    def checkData(self, table, fund_code, date):
        try:
            sql = "select * from %s where fund_code = %s and the_date = '%s'" % (table, fund_code, date)
            #print (sql)
            try:
                # Execute the SQL command
                self.cur.execute(sql)
                # Fetch all the rows in a list of lists.
                result = self.cur.fetchall()
                # 判断是否执行成功
                if result:
                    #print (self.getCurrentTime(), u"Data Insert Sucess")
                    return True
                else:
                    return False
            except Exception as e:
                # 发生错误时回滚
                self.db.rollback()
                print (self.getCurrentTime(), u"Data Check Failed: %s" % (e))
                return 0
        except Exception as e:
            print (self.getCurrentTime(), u"MySQLdb Error: %s" % (e))
            return 0
    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))