# -*- coding:utf-8 -*-

import pymysql

# Open database connection
db = pymysql.connect("localhost","root","wangxing","fund", charset='utf8')
print(db)
# prepare a cursor object using cursor() method
cursor = db.cursor()
table = 'fund_nav'
my_key = ['the_date', 'fund_code', 'fund_abbr_name']
cols = ', '.join([str(i) for i in my_key])
fund_code = '000001'
date = '2017-08-15'
# sql = "select exists(select 1 from %s where fund_code = %s and the_date = %s)" % (table, fund_code, date)
sql = "select exists(select 1 from %s where fund_code = %s and the_date = '%s')" % (table, fund_code, date)
sql = "select * from %s where fund_code = %s and the_date = '%s'" % (table, fund_code, date)
# sql = "select fund_code, fund_abbr_name from fund_info where fund_abbr_name REGEXP 'C$';"
print(sql)

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   datas = cursor.fetchall()
   print(datas)
   if datas:
      print(datas)
except:
   print("Error: unable to fecth data")

# disconnect from server
db.close()

