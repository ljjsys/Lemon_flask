from . import server
from flask import render_template, request, session, redirect
from flask.ext.login import login_required
import pymysql
from config import Config
import datetime
import json


# mysql db
mysql_server = Config.mysql_server
mysql_username = Config.mysql_username
mysql_password = Config.mysql_password
mysql_port = 3306
mysql_db = Config.mysql_db

# TypeError: datetime.date(2016, 7, 14) datetime.datetime(2015, 12, 2, 9, 51, 42)  is not JSON serializable
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            # return obj.strftime('%Y-%m-%d %H:%M:%S')
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            # return obj.strftime('%Y-%m-%d')
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


# server view
@server.route('/server')
@login_required
def server_list():
    conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_db,
                           charset='utf8')
    curs = conn.cursor()
    curs.execute('select server_id,server_hostname,server_ipaddr,server_os,server_cpu,server_memory,server_model,server_application,server_owner,created_time from server')
    server_list = curs.fetchall()
    return render_template('server/Server.html',  server_list=server_list, user_name=session.get('username'))


@server.route('/deleteServer', methods=['POST'])
def deleteServer():
    try:
        input_id = request.form['id']
        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()
        curs.execute("delete from server where server_id='%s'" % (input_id))
        data = curs.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'status': 'OK'})
        else:
            return json.dumps({'status': 'An Error occured'})

    except Exception as e:
        return json.dumps({'status': str(e)})
    finally:
        curs.close()
        conn.close()


@server.route('/updateServer', methods=['POST'])
def updateServer():
    try:
        server_id = request.form['id']
        server_application = request.form['app']
        server_owner = request.form['owner']
        server_location = request.form['location']
        server_sn = request.form['sn']
        server_remarks = request.form['remarks']
        server_warranty = request.form['warranty']

        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')
        curs = conn.cursor()

        curs.execute(
            "update server set server_owner = '%(server_owner)s', server_application = '%(server_application)s', "
            "server_location = '%(server_location)s', server_sn = '%(server_sn)s', server_remarks = '%(server_remarks)s',"
            "server_warranty='%(server_warranty)s' where server_id = '%(server_id)s'" % {
                'server_owner': server_owner,'server_application':server_application, 'server_location': server_location, 'server_sn': server_sn,
                'server_remarks': server_remarks,'server_warranty':server_warranty, 'server_id': server_id })
        data = curs.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'status': 'OK'})
        else:
            return json.dumps({'status': 'ERROR'})



    finally:

        curs.close()
        conn.close()

@server.route('/get_server_byid',methods=['POST'])
def get_server_byid():
    input_id = request.form['id']
    conn = pymysql.connect(host = mysql_server, port = mysql_port, user = mysql_username, passwd = mysql_password, db = mysql_db, charset ='utf8')
    curs = conn.cursor()
    curs.execute("select server_id,server_hostname,server_ipaddr,server_os,server_cpu,server_memory,server_model,server_application,server_owner,server_location,server_sn,server_warranty,created_time,updated_time,server_remarks from server where server_id='%s'" %(input_id))
    server_info = curs.fetchall()
    server_info_list = []
    server_info_list.append({
                'ID':server_info[0][0],
                'Hostname':server_info[0][1],
                'IP':server_info[0][2],
                'OS':server_info[0][3],
                'CPU':server_info[0][4],
                'Memory':server_info[0][5],
                'Model':server_info[0][6],
                'App':server_info[0][7],
                'Owner':server_info[0][8],
                'Location':server_info[0][9],
                'SN':server_info[0][10],
                'Warranty':server_info[0][11],
                'Created_time':server_info[0][12],
                'Updated_time':server_info[0][13],
                'Remarks':server_info[0][14]
                })
    #print (server_info_list)
    #print (json.dumps(server_info_list,cls=CJsonEncoder,ensure_ascii=False))
    #python的json.dumps方法默认会输出成这种格式"\u535a\u5ba2\u56ed",要输出中文需要指定ensure_ascii参数为False
    return json.dumps(server_info_list,cls=CJsonEncoder,ensure_ascii=False)

@server.route('/addServer', methods=['POST'])
def addServer():
    try:
        server_hostname = request.form['addHostname']
        server_ipaddr = request.form['addIP']
        server_os = request.form['addOS']
        server_cpu = request.form['addCPU']
        server_memory = request.form['addMemory']
        server_model = request.form['addModel']
        server_application = request.form['addApp']
        server_owner = request.form['addOwner']
        server_location = request.form['addLocation']
        server_sn = request.form['addSN']
        server_warranty = request.form['addWarranty']
        created_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        server_remarks = request.form['addRemarks']

        conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                               db=mysql_db, charset='utf8')

        curs = conn.cursor()
        print(server_hostname, server_ipaddr, server_os)
        curs.execute('''insert into server (server_hostname, server_ipaddr, server_os,
                        server_cpu, server_memory, server_model,server_application,server_owner,server_location,server_sn,server_warranty, created_time,server_remarks)
                        VALUES( '%(server_hostname)s', '%(server_ipaddr)s', '%(server_os)s', '%(server_cpu)s', '%(server_memory)s', '%(server_model)s', '%(server_application)s','%(server_owner)s','%(server_location)s','%(server_sn)s','%(server_warranty)s','%(created_time)s','%(server_remarks)s')''' % {
            'server_hostname': server_hostname, 'server_ipaddr': server_ipaddr, 'server_os': server_os,
            'server_cpu': server_cpu, 'server_memory': server_memory, 'server_model': server_model,
            'server_application': server_application, 'server_owner': server_owner, 'server_location': server_location,
            'server_sn': server_sn, 'server_warranty': server_warranty, 'created_time': created_time,
            'server_remarks': server_remarks})
        data = curs.fetchall()
        print(data)

        if len(data) is 0:
            conn.commit()
            return redirect('/server')
        else:
            return render_template('Errors/error.html', error='An error occurred!')

    except Exception as e:
        return render_template('Errors/error.html', error=str(e))

    finally:
        curs.close()
        conn.close()




