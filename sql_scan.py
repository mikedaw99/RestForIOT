#
#
import sqlite3
#
#
def scan_temp_log():
    conn=sqlite3.connect('freezer.sqlite')
    cursor=conn.cursor()
    cursor.execute("""select * from temp_log""")
    for row in cursor.fetchall():
        print row
    
def scan_weather():
    conn=sqlite3.connect('freezer.sqlite')
    cursor=conn.cursor()
    cursor.execute("""select * from weather""")
    for row in cursor.fetchall():
        print row
        
def create_table_weather():
    #create table
    conn=sqlite3.connect('freezer.sqlite')
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE `weather` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`datetime_logged`	DATETIME NOT NULL,
	`pressure`	VARCHAR NOT NULL,
	`temperature`	VARCHAR NOT NULL)"""
	          )
    conn.commit()
    
if __name__ == '__main__':
    #scan_temp_log()
    #scan_weather()
    create_table_weather()
    print 'finished'
    
    
