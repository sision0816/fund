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

class Strategy():
	def __init__(self, ):
		pass
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

def main():
    global mySQL
    mySQL = PyMySQL()
    mySQL._init_('localhost', 'root', 'wangxing', 'fund')
    myfund=Fund(fund_code = '003299')
    myfund.getFundInfo()
    myfund.getFundNav()
    myfund.printFundInfo()
    myfund.plotNav()


if __name__ == "__main__":
    main()
