a = 2
b = 2

if a == b:
    print('haha')

else:
    print('gaga')

print('lala')

def compare():
    if a == b:
        print('v')
    print ('w')

compare()

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return  "haha"
@app.route('/dashboard')
def dashboard():
    return "dashboard"


if __name__ == "__main__":
    app.run(debug=True)