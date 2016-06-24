from flask import Flask, render_template

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


app = Flask(__name__)
# secret key
app.secret_key = '#afdsfefefii@4#1dsfdA'

class MyForm(Form):
    username = StringField('username', validators=[DataRequired()])

@app.route('/')
def index():
    form = MyForm()
    # return '<h1>Hello World!</h1>'
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)