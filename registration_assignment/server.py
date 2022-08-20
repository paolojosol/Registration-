from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from user import User

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'first_flask'
app.secret_key = 'super secret key'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("users.html")

@app.route('/main')
def home_page():
    print(session.get('user_info'))
    if(session.get('user_info')):
        user = session['user_info']
        return render_template("main.html", user=user)
    return render_template("users.html")


@app.route('/create', methods=['POST'])
def create_user():
    if not User.validate_user(request.form, mysql):
        return redirect('/')
    else:
        User.save(request.form, mysql)
    session['user_info'] = User.get_user_info(request.form, mysql, 'email')
    return redirect('/main')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    if User.does_user_exist(request.form, mysql) and User.does_password_match(request.form, mysql) == True:
        session['user_info'] = User.get_user_info(request.form, mysql, 'login_email')

        return redirect('/main')
    elif User.does_password_match(request.form, mysql) == False:
        User.throw_password_error()
    else:
        User.throw_login_error()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
