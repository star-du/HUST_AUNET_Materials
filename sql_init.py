# 为了测试时创建数据库及相应表格参数
import sqlite3

conn = sqlite3.connect('data.db')
print ("Opened database successfully")
c = conn.cursor()
c.execute('''CREATE TABLE ADMIN
       (ID  TEXT(10)    PRIMARY KEY     NOT NULL,
       PASSWORD           TEXT(30)    NOT NULL); ''')
print ("Table admin created successfully")
ini_accounts =[('admin','au'), ('1','aaa')]
c.executemany('INSERT INTO ADMIN VALUES (?,?)', ini_accounts)
print ("admin accounts initialized successfully")
conn.commit()
conn.close()
