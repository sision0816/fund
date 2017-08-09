# -*- coding:utf-8 -*-

import pymysql

# Open database connection
db = pymysql.connect("localhost","root","wangxing","fund", charset='utf8')
print(db)
# prepare a cursor object using cursor() method
cursor = db.cursor()
table = 'fund_info'
my_key = ['fund_code', 'funder']
cols = ', '.join([str(i) for i in my_key])
sql = "select %s  from %s" % (cols, table)
print(sql)
# sql = 'select fund_code, the_date, nav, nav_chg_rate  from fund_nav;'
# sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   print(results)
except:
   print("Error: unable to fecth data")

# disconnect from server
db.close()