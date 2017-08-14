# -*- coding:utf-8 -*-

import pymysql

# Open database connection
db = pymysql.connect("localhost","root","wangxing","fund", charset='utf8')
print(db)
# prepare a cursor object using cursor() method
cursor = db.cursor()
table = 'fund_info'
my_key = ['fund_code', 'fund_abbr_name']
cols = ', '.join([str(i) for i in my_key])
sql = "select %s  from %s where fund_abbr_name REGEXP 'C$'" % (cols, table)
# sql = "select fund_code, fund_abbr_name from fund_info where fund_abbr_name REGEXP 'C$';"
print(sql)

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   datas = cursor.fetchall()
   for data in datas:
   	    print(data)
except:
   print("Error: unable to fecth data")

# disconnect from server
db.close()

# save data to file
file = open('fund_c.csv', 'w')
for data in datas:
	file.write('%s   %s\n' %(data[0], data[1]))
file.close()