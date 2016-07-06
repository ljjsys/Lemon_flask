from . import data_sync
from flask import render_template, request, session
from flask.ext.login import login_required
import pymysql
from config import Config
import datetime
from flask import json

# mysql db
mysql_server = Config.mysql_server
mysql_username = Config.mysql_username
mysql_password = Config.mysql_password
mysql_port = 3306
mysql_db = Config.mysql_db

# data_sync view
@data_sync.route('/data_sync')
@login_required
def data_sync_list():
    conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_db,
                           charset='utf8')
    curs = conn.cursor()
    curs.execute(
        'select backup_id,backup_jobname,backup_ipaddr,backup_source,backup_destination,backup_shedule,backup_owner,'
        'backup_state,last_runtime,ssh_port,backup_server from backup')
    backup_list = curs.fetchall()

    curs.execute('select backup_server_name from backup_server')
    backup_server_list = curs.fetchall()
    # backup_server_list = []
    # for backup_server in backup_list:
    #     backup_server_list.append(backup_server[10])
    #
    # backup_server_list = set(backup_server_list)
    print(backup_server_list)

    return render_template('data_sync/Data_sync.html', backup_list=backup_list, backup_server_list=backup_server_list,
                           user_name=session.get('username'))


@data_sync.route('/addBackup', methods=['POST'])
def addBackup():
    try:
        backup_jobname = request.form['jobname']
        backup_ipaddr = request.form['ipaddr']
        ssh_port = request.form['sshport']
        backup_source = request.form['source']
        backup_destination = request.form['destination']
        backup_shedule = request.form['jobminute'] + ' ' + request.form['jobhour'] + ' ' + request.form[
            'jobday'] + ' ' + request.form['jobmonth'] + ' ' + request.form['jobweek']
        backup_owner = request.form['owner']
        created_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        backup_server = request.form['backup_server']

        print(backup_jobname, backup_ipaddr, ssh_port, backup_source, backup_destination, backup_owner, created_time, backup_server)

        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()

        curs.execute('''insert into backup (backup_jobname, backup_ipaddr, ssh_port, backup_source,
                    backup_destination, backup_shedule, backup_owner, created_time, backup_server)
                    VALUES( '%(backup_jobname)s', '%(backup_ipaddr)s', '%(ssh_port)s', '%(backup_source)s',
                    '%(backup_destination)s', '%(backup_shedule)s', '%(backup_owner)s', '%(created_time)s', '%(backup_server)s')'''
                     %{'backup_jobname': backup_jobname, 'backup_ipaddr': backup_ipaddr, 'ssh_port': ssh_port,
            'backup_source': backup_source, 'backup_destination': backup_destination, 'backup_shedule': backup_shedule,
            'backup_owner': backup_owner, 'created_time': created_time, 'backup_server':backup_server})
        print('here here')
        data = curs.fetchall()

        if len(data) is 0:
            conn.commit()
            return redirect('/data_sync')
        else:
            return render_template('Errors/error.html', error='An error occurred!')
    except Exception as e:
        return render_template('Errors/error.html', error=str(e))

    finally:
        curs.close()
        conn.close()


@data_sync.route('/deleteBackup', methods=['POST'])
def deleteBackup():
    try:
        backup_id = request.form['id']
        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()
        curs.execute("delete from backup where backup_id='%s'" % (backup_id))
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

@data_sync.route('/generateCron', methods=['GET'])
def generateCron():
    subprocess.check_output(
        '/opt/python-3.5.1/bin/python3 /root/Projects/data_sync/data_sync_master/backup/backup_master.py', shell=True)
    return "haha"