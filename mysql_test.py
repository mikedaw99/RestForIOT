#!/usr/bin/env python
import mysql.connector

config = {}
config['user'] = 'dawsonm'
config['password'] = 'jupiter1'
config['host'] = 'mysqlsensorlogdb.chxaueqhhlie.eu-west-1.rds.amazonaws.com'
config['database'] = 'mwd'

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
cursor.execute(
	      """select * from weather""")

for row in cursor:
    print row
    

cursor.close()
cnx.close()