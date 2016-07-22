#!/usr/bin/env python

import urllib.request
import json
import datetime
import pymysql

# mysql db
mysql_server = '10.48.192.162'
mysql_username = 'lemon'
mysql_password = 'memory'
mysql_port = 3306
mysql_db = 'Lemon_GO'

rest_api_url = 'http://10.48.192.162:8888/server_info'

try:
    server_info_bytes =  urllib.request.urlopen(rest_api_url)
    
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.read().decode("utf8"))
  
server_info_string = server_info_bytes.read().decode('utf-8')
server_info_dict = json.loads(server_info_string)

#for k,v in server_info_dict.items():
#       print(k,v)

try:
    conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password,
                       db=mysql_db, charset='utf8')
    curs = conn.cursor()
    for salt_minion_name in  server_info_dict:
        server_hostname = server_info_dict[salt_minion_name]['nodename']
        server_ipaddr = server_info_dict[salt_minion_name]['ip4_interfaces:eth0'][0]
        server_os = server_info_dict[salt_minion_name]['os'] + '-' + server_info_dict[salt_minion_name]['osrelease'] + '-' + server_info_dict[salt_minion_name]['osarch']
        server_cpu = str(server_info_dict[salt_minion_name]['num_cpus']) + ' * ' + server_info_dict[salt_minion_name]['cpu_model'] 
        server_memory = server_info_dict[salt_minion_name]['mem_total']
        server_model = server_info_dict[salt_minion_name]['virtual']
        created_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        print(server_hostname,server_ipaddr,server_os,server_cpu,created_time)
	
	# if records exists, update , hostname and ip must unique
#         curs.execute('''insert into server (server_hostname, server_ipaddr, server_os,
#             server_cpu, server_memory, server_model, created_time)
#             VALUES( '%(server_hostname)s', '%(server_ipaddr)s', '%(server_os)s', '%(server_cpu)s', '%(server_memory)s',
#              '%(server_model)s', '%(created_time)s')
# on duplicate key update server_cpu='%(server_cpu)s', server_memory='%(server_memory)s' ''' % {
#     'server_hostname':server_hostname, 'server_ipaddr':server_ipaddr, 'server_os':server_os,'server_cpu':server_cpu,
#             'server_memory':server_memory, 'server_model':server_model, 'created_time': created_time })
        curs.execute('''replace into server (server_hostname, server_ipaddr, server_os,
            server_cpu, server_memory, server_model, created_time)
            VALUES( '%(server_hostname)s', '%(server_ipaddr)s', '%(server_os)s', '%(server_cpu)s', '%(server_memory)s',
             '%(server_model)s', '%(created_time)s') ''' % {
    'server_hostname':server_hostname, 'server_ipaddr':server_ipaddr, 'server_os':server_os,'server_cpu':server_cpu,
            'server_memory':server_memory, 'server_model':server_model, 'created_time': created_time })
        data = curs.fetchall()
    
        if len(data) is 0:
            conn.commit()
            print('Insert record OK')

except Exception as e:
    print(str(e))
        
finally:
    curs.close()
    conn.close()
