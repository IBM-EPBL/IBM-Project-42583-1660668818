from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re
app=Flask(__name__)
app.secret_key='a'
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLSERVERCERIFICATE=DigiCertGlobalRootCA.crt;UID=fqg93621;PWD=eezWMIvhvTceZxPH",'','')

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/login",methods=['GET','POST'])
def login():
    global userid
    msg =''

    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE username = ? AND password = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['username']
            userid= account['USERNAME']
            session['username']=account['USERNAME']
            msg='Logged in successfully!'
            return render_template('page.html',msg=msg)
        else:
            msg='Incorrect username/password'
            return render_template('login.html',msg=msg)
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE username = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg="Invalid email address"
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg="Name must contain characters and numbers"
        else:
                insert_sql="INSERT INTO user VALUES(?,?,?)"
                prep_stmt= ibm_db.prepare(conn.insert_sql)
                ibm_db.bind_param(prep_stmt,1,username)
                ibm_db.bind_param(prep_stmt,2,email)
                ibm_db.bind_param(prep_stmt,3,password)
                ibm_db.execute(prep_stmt)
                msg="You have successfully registered"
    elif request.method=="POST":
        msg="Please fill out the form"
        return render_template("registration.html",msg=msg)

@app.route('/page')
def page():
    return render_template("page.html")

@app.route('/apply',methods=['GET','POST'])
def app():
    msg=''
    if request.method=="POST":
        username=request.form['username']
        email=request.form['email']
        rollnumber=request.form['rollnumber']
        password=request.form['password']
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)

        if account():
            return render_template('page.html')

        insert_sql="INSERT INTO user VALUES(?,?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,username)
        ibm_db.bind_param(prep_stmt,2,email)
        ibm_db.bind_param(prep_stmt,3,rollnumber)
        ibm_db.bind_param(prep_stmt,4,password)
        ibm_db.execute(prep_stmt)





        
