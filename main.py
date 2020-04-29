from flask import Flask
from flask import render_template
from flask import url_for
from flask_bootstrap import Bootstrap

import pymysql

connection = pymysql.connect(host='127.0.0.1',
                            user='aspen',
                            password='Dragon12',
                            db='test')

print (connection)

# with connection.cursor() as cursor:
#     sql = "CREATE TABLE testTable (id INT(6) primary key, firstname varchar(30) not null, email varchar(50))"
#     cursor.execute(sql)


with connection.cursor() as cursor:
    sql = "SELECT * from testTable"
    cursor.execute(sql)
    result = cursor.fetchone()
    print (result)

app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')