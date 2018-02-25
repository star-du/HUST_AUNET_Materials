# 为了测试时创建数据库及相应表格参数
import sqlite3

conn = sqlite3.connect('data.db')
print ("Opened database successfully")
c = conn.cursor()

c.execute('''CREATE TABLE ADMIN
       (ID  TEXT(10)    PRIMARY KEY     NOT NULL,
       PASSWORD           TEXT(30)    NOT NULL); ''')
print ("Table admin created successfully")
# ini_accounts =[('admin','au'), ('1','aaa'), ('I_AM_BOSS','showmethemoney'),('村下没有树','666')]
# c.executemany('INSERT INTO ADMIN VALUES (?,?)', ini_accounts)
# print ("admin accounts initialized successfully")

c.execute('''CREATE TABLE ADMIN2
       (ID  TEXT(10)    PRIMARY KEY     NOT NULL,
       PASSWORD           TEXT(30)    NOT NULL); ''')
print ("Table admin2 created successfully")
# ini_accounts =[('sudo','pass'), ('class','qwert')]
# c.executemany('INSERT INTO ADMIN2 VALUES (?,?)', ini_accounts)
# print ("admin2 accounts initialized successfully")
# used to store accounts of adminster overseeing classroom_apply


c.execute('''CREATE TABLE MATERIAL
       (ID  INTEGER    PRIMARY KEY     AUTOINCREMENT,
       DEP     TEXT    NOT NULL,
       NAME    TEXT    NOT NULL,
       MATERIAL TEXT   NOT NULL,
       CONTACT TEXT    NOT NULL,
       STARTYEAR   INTEGER    NOT NULL,
       STARTMONTH   INTEGER    NOT NULL,
       STARTDAY   INTEGER    NOT NULL,
       STARTHOUR   INTEGER    NOT NULL,
       ENDINGYEAR  INTEGER    NOT NULL,
       ENDINGMONTH  INTEGER    NOT NULL,
       ENDINGDAY  INTEGER    NOT NULL,
       ENDINGHOUR  INTEGER    NOT NULL,
       STATUS  INTEGER NOT NULL,
       ADMIN   TEXT ); ''')
print ("Table material created successfully")
# 数据库内各项依次表示 处理申请序号、申请人部门、姓名、申请者材料、联系方式、紧随的8项为相应时间、其后是审批状态与审批者信息
# 其中id为自动递增，加入数据时 **无需显式填写**
# START- 与 END- 开头的各项为借出与归还的时间
# status 用0表示未处理，1表示审批未通过， 2表示审批通过
# ADMIN 如经过审批，将审批的管理员id记录

c.execute('''CREATE TABLE CLASSROOM
       (ID  INTEGER    PRIMARY KEY     AUTOINCREMENT,
       DEP     TEXT    NOT NULL,
       NAME    TEXT    NOT NULL,
       CLASSROOM TEXT   NOT NULL,
       CONTACT TEXT    NOT NULL,
       STARTYEAR   INTEGER    NOT NULL,
       STARTMONTH   INTEGER    NOT NULL,
       STARTDAY   INTEGER    NOT NULL,
       STARTHOUR   INTEGER    NOT NULL,
       ENDINGYEAR  INTEGER    NOT NULL,
       ENDINGMONTH  INTEGER    NOT NULL,
       ENDINGDAY  INTEGER    NOT NULL,
       ENDINGHOUR  INTEGER    NOT NULL,
       STATUS  INTEGER NOT NULL,
       ADMIN   TEXT ); ''')
print ("Table classroom created successfully")
# 与material类似，仅将material项替换为CLASSROOM

conn.commit()

conn.close()
