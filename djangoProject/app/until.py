import pymysql
from config import Config

def coon():
    con = pymysql.connect(host=Config.Host, port=Config.Port, user=Config.User, password=Config.Password, db=Config.Database)
    cur = con.cursor()
    return con, cur

def close(con, cur):
    if cur:
        cur.close()
    if con:
        con.close()

def qurey(sql):
    con, cur = coon()
    try:
        cur.execute(sql)
        res = cur.fetchall()
        return res
    finally:
        close(con, cur)

def insert(sql):
    con, cur = coon()
    try:
        cur.execute(sql)
        con.commit()
    finally:
        close(con, cur)