from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import ibm_db
import random
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '200109'

# Enter your database connection details below

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLSERVERCERIFICATE=DigiCertGlobalRootCA.crt;UID=fqg93621;PWD=eezWMIvhvTceZxPH")


@app.route('/test')
def test():
    return render_template('loginregister.html')


@app.route('/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        # getting user data
        email = request.form.get('username')
        password = request.form.get('password')
        sql_check_query = "SELECT * FROM users WHERE username = ?"
        stmt = ibm_db.prepare(conn, sql_check_query)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            # email id exists 
            # checking if the password is correct
            if not account['PASSWORD'] == password:
                flash('Invalid password', category='error')

            else:
                # user entered the correct password
                # redirecting the user to the dashboard
                session['USERNAME'] = account['USERNAME']
                session['loggedin'] = True
                return redirect('/index')

        else:
            # email id does not exist in the database
            flash('Email invalid... Try Again', category='error')
            
        return render_template('loginregister.html')
    
    return render_template('loginregister.html')



# http://localhost:5000/pythinlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@app.route('/loginregister', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        # getting user data
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        # checking: user already exists or not
        sql_check_query = "SELECT * FROM users WHERE email = ?"
        stmt = ibm_db.prepare(conn, sql_check_query)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt) 

        account = ibm_db.fetch_assoc(stmt)
        # email id does not exist in the database
        if not account:
            # inserting the data into the database
            sql_insert_query = "INSERT INTO users VALUES (?, ?, ?)"
            stmt = ibm_db.prepare(conn, sql_insert_query)
            ibm_db.bind_param(stmt, 1, email)
            ibm_db.bind_param(stmt, 2, password)
            ibm_db.bind_param(stmt, 3, username)
            ibm_db.execute(stmt)

            # user data inserted into the database
            # redirecting to login page
            flash('User created successfully! Please Login', category='success')
            return redirect('/')

        else:
            flash('Email id already exists! Try another one', category='error')

        return render_template('loginregister.html')

    return render_template('loginregister.html')

@app.route('/index', methods=['GET'])
def home():

    # Check if user is loggedin
    if 'loggedin' in session:
                  
        return render_template('index.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('loginregister'))    


@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   session.pop('email', None)
   return render_template('loginregister.html')
     


if __name__ =='__main__':
	app.run(debug=True)
