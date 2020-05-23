import pymysql
from flask import g, current_app


def getConn():
    '''create a new d/b connection or get it from global dictionary
    '''
    if 'conn' not in g:
        host, user, pswd, db = map(
            current_app.config.get, 
            ['MYSQL_HOST', "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"]
        )
        g.conn = pymysql.connect(host, user, pswd, db)
    return g.conn

def closeConn():
    '''close the d/b connection
    '''
    conn = g.pop("conn", None)
    if conn is not None:
        conn.close()
