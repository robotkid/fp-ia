from flask import Flask, render_template,request,flash,redirect,session,url_for
from app import app, db
from formsubmission import BrawlStarsMapTrackerRegistrationForm 

app = Flask(__name__)
app.secret_key="__privatekey__"

@app.route('/')
def defaultHome():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        userName = request.form['name']
        userPassWord=request.form['passWord']
        if userName=='admin'and userPassWord=='admin123':
            return render_template('dashboard.html', name=userName)  
        else:
            return render_template('home.html')
    else:
        userName=request.args.get('name')
        return render_template('login.html', name=userName)

@app.route('/registrationform', methods=['POST', 'GET'])
def registrationform():
    brawlStarsMapTrackerRegistrationForm=BrawlStarsMapTrackerRegistrationForm()
    if request.method=='POST':
        session['name']=request.form['name']
        if brawlStarsMapTrackerRegistrationForm()=="False":
            flash("Please fill out this field")
            return render_template('register.html', form=brawlStarsMapTrackerRegistrationForm)
        else:
            return redirect(url_for('successformsubmission'))
    elif request.method == "GET":
        return render_template('register.html', form=brawlStarsMapTrackerRegistrationForm)

@app.route('/successformsubmission')
def successformsubmission():
    name=session.get('name', None)
    return render_template('successformsubmission.html')
