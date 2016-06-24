from flask import Flask,request
from flaskext.mysql import MySQL
#from  flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'lemon'
app.config['MYSQL_DATABASE_PASSWORD'] = 'memory'
app.config['MYSQL_DATABASE_DB'] = 'lemon_go'
app.config['MYSQL_DATABASE_HOST'] = '166.6.6.10'
mysql.init_app(app)

@app.route("/")
def hello():
    return "Welcome to Python Flask App!"

@app.route("/login")
def Authenticate():
    username = request.args.get('username')
    password = request.args.get('password')
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * from users  where username='" + username + "' and password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"

if __name__ == '__main__':
    app.run(
            host="0.0.0.0",
            port=8888,
            debug=True ) #console, debug=False
