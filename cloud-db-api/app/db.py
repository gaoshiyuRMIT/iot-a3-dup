import pymysql
from flask import g, current_app


def getConn():
    if 'conn' not in g:
        host, user, pswd, db = map(
            current_app.config.get, 
            ['MYSQL_HOST', "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"]
        )
        g.conn = pymysql.connect(host, user, pswd, db)
    return g.conn

def closeConn():
    conn = g.pop("conn", None)
    if conn is not None:
        conn.close()
