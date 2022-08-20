from flask import flash
from io import StringIO
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__( self , data ):
        self.id = data[0]
        self.first_name = data[1]
        self.last_name = data[2]
        self.email = data[3]
        self.password = data[4]

    @classmethod
    def get_user(cls, mysql, email):        
        str_build = StringIO()
        str_build.write("SELECT * FROM users where email='")
        str_build.write(email)
        str_build.write("'")
        str_build.write(";")
        # make sure to call the connectToMySQL function with the schema you are targeting.
        cur = mysql.connection.cursor()
        cur.execute(str_build.getvalue())
        users = cur.fetchall()
        return users


    @classmethod
    def does_user_exist(cls, user, mysql):
        get_email_users = cls.get_user(mysql, user['login_email'])
        return len(get_email_users) > 0

    @classmethod
    def does_password_match(cls, user, mysql):
        is_valid = True
        get_email_users = cls.get_user(mysql, user['login_email'])
        users = []
        if len(get_email_users) > 0:
            for u in get_email_users:
                users.append( cls(u) )
            cur_user = users[0]
            if getattr(cur_user, 'password') != user['login_password']:
                is_valid = False
        return is_valid

    @classmethod
    def get_user_info(cls, user, mysql, field):
        get_email_users = cls.get_user(mysql, user[field])
        users = []
        if len(get_email_users) > 0:
            for u in get_email_users:
                users.append( cls(u) )
            cur_user = users[0]
            return getattr(cur_user, 'first_name')


    # Other Burger methods up yonder.
    # Static methods don't have self or cls passed into the parameters.
    # We do need to take in a parameter to represent our burger
    @classmethod
    def validate_user(cls,user, mysql):
        is_valid = True # we assume this is true
        get_email_users = cls.get_user(mysql, user['email'])
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("password and confirm password must be the same.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("password must be at least 8 characters.", "register")
            is_valid = False
        if len(get_email_users) > 0:
            flash("The email already exist in the database. Please try a different one.", "register")
            is_valid = False

        return is_valid
    
    @classmethod
    def throw_login_error(cls):
        flash("This email does not exist. Please try again.", "login")

    @classmethod
    def throw_password_error(cls):
        flash("The passwords do not match. Please try again.", "login")

    @classmethod
    def save(cls, data, mysql):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        str_build = StringIO()
        str_build.write("INSERT INTO users (first_name,last_name,email, password) VALUES ('")
        str_build.write(first_name)
        str_build.write("'")
        str_build.write(",'")
        str_build.write(last_name)
        str_build.write("'")
        str_build.write(",'")
        str_build.write(email)
        str_build.write("'")
        str_build.write(",'")
        str_build.write(password)
        str_build.write("'")
        str_build.write(");")

        query = str_build.getvalue()
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        result = cur.fetchone()
        print(result)
        return result