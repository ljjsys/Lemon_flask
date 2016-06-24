from . import user
from flask import render_template, request, session
from flask.ext.login import login_required
import pymysql
from config import Config
from werkzeug import generate_password_hash, check_password_hash
import datetime

# mysql db
mysql_server = Config.mysql_server
mysql_username = Config.mysql_username
mysql_password = Config.mysql_password
mysql_port = 3306
mysql_db = Config.mysql_db



@user.route('/user_manage')
@login_required
def user_manage():
    conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_db,
                           charset='utf8')
    curs = conn.cursor()
    curs.execute('select id,user_name,email,created_time,role_id from users')
    user_list = curs.fetchall()
    print(user_list)
    return render_template('user/user_manage.html', user_list=user_list, user_name=session.get('username'))


@user.route('/addUser', methods=['POST'])
def addUser():
    try:
        print("bbbbb")
        user_name = request.form['username']
        print(user_name)
        email = request.form['email']
        print(email)
        _password = request.form['password']
        print(_password)
        user_password = generate_password_hash(_password)

        print(user_password)

        user_group = request.form['group']
        print(user_group)
        created_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        print(created_time)

        print(user_name)

        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()
        curs.execute('''insert into users (user_name, email, password_hash, created_time)
        VALUES( '%(user_name)s', '%(email)s', '%(password_hash)s', '%(created_time)s')''' % {
            'user_name': user_name, 'email': email, 'password_hash': user_password, 'created_time': created_time})
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
        curs.execute("delete from users where id='%s'" % (id))
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
    id = request.form['id']
    conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_db,
                           charset='utf8')
    curs = conn.cursor()
    curs.execute("select id,user_name,email,user_group from users where id='%s'" % (id))
    user_info = curs.fetchall()
    print(user_info)
    user_info_list = []
    user_info_list.append({
        'ID': user_info[0][0],
        'username': user_info[0][1],
        'email': user_info[0][2],
        'group': user_info[0][3],
    })
    return json.dumps(user_info_list, cls=CJsonEncoder, ensure_ascii=False)


@user.route('/updateUser', methods=['POST'])
def updateUser():
    try:
        id = request.form['id']
        email = request.form['email']
        user_group = request.form['group']

        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()
        curs.execute(
            "update users set email = '%(email)s', user_group = '%(user_group)s' where id = '%(id)s'" % {
                'email': email, 'user_group': user_group, 'id': id})
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