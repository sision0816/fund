# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 09:06:57 2017

@author: xing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#pylab.rcParams['figure.figsize'] = (10, 6) #设置绘图尺寸

#read data
fund = pd.read_table('fund000001.csv', usecols=range(5), parse_dates=[0], index_col=0)
fund = fund[::-1] #inverse
print(fund.head())
print(fund.info())
print(fund.columns)


fund['单位净值'].plot()



