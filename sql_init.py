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

c.execute('''CREATE TABLE MATERIAL
       (ID  INTEGER    PRIMARY KEY     AUTOINCREMENT,
       DEP     TEXT    NOT NULL,
       NAME    TEXT    NOT NULL,
       MATERIAL TEXT   NOT NULL,
       CONTACT TEXT    NOT NULL,
       STARTYEAR   INT    NOT NULL,
       STARTMONTH   INT    NOT NULL,
       STARTDAY   INT    NOT NULL,
       STARTHOUR   INT    NOT NULL,
       ENDINGYEAR  TEXT    NOT NULL,
       ENDINGMONTH  TEXT    NOT NULL,
       ENDINGDAY  TEXT    NOT NULL,
       ENDINGHOUR  TEXT    NOT NULL,
       STATUS  INTEGER NOT NULL,
       ADMIN   TEXT ); ''')
print ("Table material created successfully")
# 数据库内各项依次表示 处理申请序号、申请人部门、姓名、申请者材料、联系方式
# START- 与 END- 开头的各项为借出与归还的时间
# status 用0表示未处理，1表示审批未通过， 2表示审批通过
# ADMIN 如经过审批，将审批的管理员id记录

conn.commit()

conn.close()
