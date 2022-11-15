from flask import Flask, render_template,request

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("registration.html")
@app.route("/confirm",methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        n =request.form.get('username')
        e =request.form.get('email')
        p =request.form.get('phone')
        return render_template('confirm.html',username=n,email=e,phone=p)
    

if __name__=="__main__":
    app.run(debug=True)