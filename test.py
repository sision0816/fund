# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:56:21 2017

@author: xing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

s = pd.Series([1, 2, 3, 5, 8])
print(s)

datas = pd.date_range('20170701', periods = 6)
print(datas)

df = pd.DataFrame(np.random.randn(6, 4), index=datas, columns=list('ABCD'))
print(df)



