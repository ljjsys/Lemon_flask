from . import data_sync
from flask import render_template, request, session, redirect
from flask.ext.login import login_required
import pymysql
from config import Config
import datetime
from flask import json
import subprocess

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

    curs.execute('select server_name from backup_server')
    backup_server_list = curs.fetchall()
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

        data = curs.fetchall()

        if len(data) is 0:
            conn.commit()
            user_create = subprocess.check_call(
                "salt '%(backup_jobname)s' cmd.run 'groupadd -g 6000 backup && useradd -u 6000 -g 6000 backup'" % {
                    'backup_jobname': backup_jobname},
                shell=True)
            print(user_create)
            subprocess.check_call("salt 'test-client.mgtest.com' ssh.set_auth_key_from_file backup salt://ssh_keys/backup_id_rsa.pub" ,shell=True)

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

@data_sync.route('/add_BackupServer', methods=['POST'])
def addBackupServer():
    try:
        server_name = request.form['server_name']
        ipaddress = request.form['ipaddress']
        backup_folder = request.form['backup_folder']
        backup_user = request.form['backup_user']

        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()

        curs.execute('''insert into backup_server (server_name, ipaddress, backup_folder, backup_user)
                    VALUES( '%(server_name)s', '%(ipaddress)s', '%(backup_folder)s', '%(backup_user)s')'''
                     %{'server_name': server_name, 'ipaddress': ipaddress, 'backup_folder': backup_folder, 'backup_user': backup_user})
        data = curs.fetchall()

        if len(data) is 0:
            conn.commit()
        else:
            return render_template('Errors/error.html', error='An error occurred! Please check log.')
        user_create = subprocess.check_call("salt '%(server_name)s' cmd.run 'groupadd -g 6000 backup && useradd -u 6000 -g 6000 backup'" % {'server_name': server_name},
                                shell=True)
        print(user_create)

        ssh_key_create = subprocess.check_call("salt '%(server_name)s' lemon_module.create_ssh_user_key backup" % {'server_name': server_name},
                                shell=True)
        print(ssh_key_create)
        return "status: Ok."

    except Exception as e:
        return render_template('Errors/error.html', error=str(e))
    finally:
        curs.close()
        conn.close()


@data_sync.route('/generateCron', methods=['POST'])
def generateCron():
    backup_server = request.form['backup_server']
    conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_db,
                           charset='utf8')
    curs = conn.cursor()
    curs.execute(
        "select backup_jobname,backup_ipaddr,ssh_port,backup_source,backup_destination,backup_shedule,backup_id,backup_server from backup "
        "where backup_server='%(backup_server)s'" %{'backup_server': backup_server})
    backup_list = curs.fetchall()

    print(backup_list)
    # with open('/srv/salt/crons/cron', 'w') as f:
    #     pass
    cron_list = []
    for backup in backup_list:
        backup_user = 'backup'
        cron_shedule = backup[5]
        backup_ip = backup[1]
        ssh_port = backup[2]
        backup_source = backup[3]
        backup_destination = backup[4]
        backup_id = backup[6]
        cron_cmd = '''/opt/lemon_agent/data_sync/rsync.sh -p %(ssh_port)s -s %(backup_user)s@%(backup_ip)s:%(backup_source)s \
-d %(backup_destination)s -i %(backup_id)s''' % {
            'backup_user': backup_user, 'backup_ip': backup_ip, 'ssh_port': ssh_port, 'backup_source': backup_source,
            'backup_destination': backup_destination, 'backup_id': backup_id }
        print (cron_cmd)
        cron_list.append(cron_shedule + ' ' + cron_cmd + '\n')
    print(cron_list)
    with open('/srv/salt/crons/%s_%s.cron' %(backup_server,backup_user ) ,'w') as f:
        f.writelines(cron_list)
    subprocess.check_call(
            "salt '%(backup_server)s' cp.get_file salt://crons/%(backup_server)s_%(backup_user)s.cron /tmp/%(backup_server)s_%(backup_user)s.cron"
            % {'backup_server': backup_server, 'backup_user':backup_user},shell=True)
        # with open('/srv/salt/crons/cron', 'a') as f:
        #     f.write(cron_shedule + ' ' + cron_cmd + '\n')
    subprocess.check_call(
        "salt '%(backup_server)s' cron.write_cron_file_verbose %(backup_user)s /tmp/%(backup_server)s_%(backup_user)s.cron"
        % {'backup_server': backup_server, 'backup_user': backup_user}, shell=True)
    # subprocess.check_output(
    #     '/opt/python-3.5.1/bin/python3 /root/Projects/data_sync/data_sync_master/backup/backup_master.py', shell=True)
    return 'haha'

