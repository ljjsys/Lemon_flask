from . import user
from flask import render_template, request, session
from flask.ext.login import login_required
import pymysql
from config import Config
from werkzeug import generate_password_hash, check_password_hash
import datetime
from flask import json

# mysql db
mysql_server = Config.mysql_server
mysql_username = Config.mysql_username
mysql_password = Config.mysql_password
mysql_port = 3306
mysql_db = Config.mysql_db

# user view
@user.route('/user_manage')
@login_required
def user_manage():
    try:
        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_db,
                               charset='utf8')
        curs = conn.cursor()
        curs.execute('''
                      SELECT users.id,user_name,user_email,created_time,role_name
                      FROM users INNER JOIN roles ON users.`role_id` = roles.`id`
                      ''')
        user_list = curs.fetchall()
        print(user_list)
        curs.execute("select role_name from roles")
        role_list = curs.fetchall()
        print(role_list[0][0])
        return render_template('user/user_manage.html', user_list=user_list, role_list=role_list, user_name = session.get('username'))
    finally:
        curs.close()
        conn.close()

@user.route('/addUser',methods=['POST'])
def addUser():
    try:
        user_name = request.form['username']
        user_email = request.form['email']
        _password = request.form['password']
        user_password = generate_password_hash(_password)
        role_name = request.form['role']
        created_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()
        curs.execute('''insert into users (user_name, user_email, password_hash, created_time, role_id)
                        VALUES( '%(user_name)s', '%(user_email)s', '%(password_hash)s', '%(created_time)s',
                         (SELECT id FROM roles WHERE role_name = '%(role_name)s'))''' % {
            'user_name': user_name, 'user_email': user_email, 'password_hash': user_password,  'created_time': created_time, 'role_name':role_name})
        data = curs.fetchall()

        if len(data) is 0:
            conn.commit()
            return redirect('/user_manage')
        else:
            return render_template('Errors/error.html', error='An error occurred!')
    except Exception as e:
        return render_template('Errors/error.html', error=str(e))

    finally:
        curs.close()
        conn.close()

@user.route('/deleteUser', methods=['POST'])
def deleteUser():
    try:
        id = request.form['id']
        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()
        curs.execute("delete from users where id='%s'" % id)
        data = curs.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'status': 'OK'})
        else:
            return json.dumps({'status': 'An Error occured'})

    except Exception as e:
        return json.dumps({'status': str(e)})
    finally:
        print('final')
        curs.close()
        conn.close()

@user.route('/get_user_byid', methods=['POST'])
def get_user_byid():
    user_id = request.form['id']
    conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_db,
                           charset='utf8')
    curs = conn.cursor()
    curs.execute("select users.id,user_name,user_email,role_name FROM users INNER JOIN roles "
                 "ON users.role_id = roles.id where users.id = '%s'" % user_id)
    user_info = curs.fetchall()
    user_info_list = []
    user_info_list.append({
        'ID': user_info[0][0],
        'username': user_info[0][1],
        'email': user_info[0][2],
        'role': user_info[0][3],
    })
    print(user_info_list)
    return json.dumps(user_info_list)

@user.route('/updateUser', methods=['POST'])
def updateUser():
    try:
        id = request.form['id']
        user_email = request.form['email']
        user_role = request.form['role']

        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()
        curs.execute(
            "update users set user_email = '%(user_email)s', user_role = '%(user_role)s' where id = '%(id)s'" % {
                'user_email': user_email, 'user_role': user_role, 'id': id})
        data = curs.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'status': 'OK'})
        else:
            return json.dumps({'status': 'ERROR'})

    except Exception as e:
        return json.dumps({'status': 'Unauthorized access'})

    finally:
        curs.close()
        conn.close()