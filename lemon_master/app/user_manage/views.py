from . import user_manage
from flask import render_template, request, session
from flask.ext.login import login_required
import pymysql
from config import Config

# mysql db
mysql_server = Config.mysql_server
mysql_username = Config.mysql_username
mysql_password = Config.mysql_password
mysql_port = 3306
mysql_db = Config.mysql_db

@user_manage.route('/haha')
def haha():
    return "ggo"

@user_manage.route('/lala')
def lala():
    return "lala"

@user_manage.route('/user_manage')
@login_required
def user_manage():
    conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_db,
                           charset='utf8')
    curs = conn.cursor()
    curs.execute('select id,user_name,email,created_time,role_id from users')
    user_list = curs.fetchall()
    print(user_list)
    return render_template('user_manage.html', user_list=user_list, user_name=session.get('username'))

