import pymysql

# connect to mysql
conn = pymysql.connect(host=mysql_server, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_db)
curs = conn.cursor()


def mysql_select(sql):
    curs.execute(sql)
    result = curs.fetchall()
    return result


db_username = mysql_select("SELECT user_name FROM user WHERE user_name='%s'" % (input_username))[0][0]
db_password = mysql_select("SELECT user_password FROM user WHERE user_name='%s'" % (input_username))[0][0]
print(db_password)
print(check_password_hash(str(db_password), input_password))

curs.execute("delete from server where server_id='%s'" %(input_id))

conn.commit()
curs.close()
conn.close()