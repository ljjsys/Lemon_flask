from flask import Flask,request
#from flaskext.mysql import MySQL
from flask.ext.mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'lemon'
app.config['MYSQL_PASSWORD'] = 'memory'
app.config['MYSQL_DB'] = 'Lemon'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route("/")
def hello():
    return "Welcome to Python Flask App!"

@app.route("/login")
def Authenticate():
    username = request.args.get('username')
    password = request.args.get('password')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from user  where user_name='" + username + "' and user_password='" + password + "'")
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
