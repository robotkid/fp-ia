from flask import Flask, flash, render_template, request, session, redirect, url_for
import requests
import json 
#https://cs50.readthedocs.io/libraries/cs50/python/
from cs50 import SQL
import sqlite3
import smtplib
#https://www.youtube.com/watch?v=z0AfnEPyvAs
from flask_apscheduler import APScheduler
from notifications import notify_users
from formsubmission import BrawlStarsMapTrackerRegistrationForm
#db=SQL("sqlite:///data.db")
app = Flask(__name__)
app.secret_key="__privatekey__"
scheduler = APScheduler()

res = requests.get('https://api.brawlify.com/v1/events')
response = json.loads(res.text)

#https://stackoverflow.com/questions/31270488/navigating-json-in-python

#source - https://stackoverflow.com/questions/68429566/how-to-return-render-template-in-flask
#videos for login/registration: https://youtu.be/fPAUGZYU4MA?feature=shared
#https://www.youtube.com/watch?v=YpKYBG38FbM&list=PLf9umJdQ546h26s7VKQVUir5GoOZ-1JTP&index=12
@app.route("/")

def defaultHome():
    brawlStarsMapTrackerRegistrationForm=BrawlStarsMapTrackerRegistrationForm()
    return render_template('login.html',form=brawlStarsMapTrackerRegistrationForm)

def fetch_active_map_names():
    active_maps = response.get("active", [])
    active_map_names = [map_info["map"]["name"] for map_info in active_maps if "map" in map_info]
    return active_map_names

def fetch_upcoming_map_names():
    upcoming_maps = response.get("upcoming", [])
    upcoming_map_names = [map_info["map"]["name"] for map_info in upcoming_maps if "map" in map_info]
    return upcoming_map_names
    
active_map_names = fetch_active_map_names()
print("Active maps:", active_map_names)

upcoming_map_names = fetch_upcoming_map_names()
print("Upcoming maps:", upcoming_map_names)

def create_table():
    con = sqlite3.connect('user1.db')
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user1(name text, passWord text, email text)")
    c.execute("CREATE TABLE IF NOT EXISTS currentMaps(map_name text)")
    c.execute("CREATE TABLE IF NOT EXISTS favoriteMaps(user_name text, map_name text)")
    c.execute("CREATE TABLE IF NOT EXISTS notifications (map_name text,user_name text,notified_date text)")
    con.commit()
    con.close()

create_table()

@app.route('/home', methods=['POST','GET'])
def home():
        if 'username' not in session:
             return redirect('/login')
        username = session['username']
        print(f"User logged in: {username}")
        con = sqlite3.connect('user1.db')
        c = con.cursor()
        c.execute("SELECT map_name FROM favoriteMaps WHERE user_name = ?", (username,))
        user_favorites = [row[0] for row in c.fetchall()]
        c.execute("SELECT email FROM user1 WHERE name = ?", (username,))
        user_email = c.fetchone()
        if user_email:
            user_email = user_email[0]
        message = None
        if request.method == 'POST':
            map_name = request.form.get('addMaps')
            email = request.form.get('setEmail')
            print(f"Map entered by user: {map_name}")
            if map_name:
                if map_name in active_map_names or  map_name in upcoming_map_names:
                    c.execute("SELECT * FROM favoriteMaps WHERE user_name = ? AND map_name = ?", (username, map_name))
                    if c.fetchone():
                        message = f"'{map_name}' is already in your favorites."
                    else:
                        c.execute("INSERT INTO favoriteMaps (user_name, map_name) VALUES (?, ?)", (username, map_name))
                        con.commit()
                        message = f"'{map_name}' has been added to your favorites."
                        c.execute("SELECT map_name FROM favoriteMaps WHERE user_name = ?", (username,))
                        user_favorites = [row[0] for row in c.fetchall()]
                else:
                    message = f"'{map_name}' is not an active or upcoming map."
            else:
                message = "Please enter a valid map name."

            if email:
                c.execute("UPDATE user1 SET email = ? WHERE name = ?", (email, username))
                con.commit()
                message = f"Email {email} has been set for notifications."
                    
        con.close()
        brawlStarsMapTrackerRegistrationForm = BrawlStarsMapTrackerRegistrationForm()
        return render_template(
            'index.html',
            form=brawlStarsMapTrackerRegistrationForm,
            favorites=user_favorites,
            active_maps=active_map_names,
            upcoming_maps=upcoming_map_names,
            message=message,
            username=username,
            email=user_email
        )
@app.route('/remove_favorite/<map_name>', methods=['POST'])
def remove_favorite(map_name):
    if 'username' not in session:
        return redirect('/login')
    username = session['username']
    con = sqlite3.connect('user1.db')
    c = con.cursor()
    c.execute("DELETE FROM favoriteMaps WHERE user_name = ? AND map_name = ?", (username, map_name))
    con.commit()
    return redirect('/home')
  
@app.route('/login', methods=['POST','GET'])
def login():
     if request.method=='POST':
        userName = request.form['name']
        passWord=request.form['passWord']
        con=sqlite3.connect('user1.db')
        c=con.cursor()
        statement=f"SELECT * from user1 WHERE name='{userName}' AND passWord='{passWord}';"
        c.execute(statement)
        user = c.fetchone()
        if user:
            session['username'] = userName
            return redirect('/home')
        else:
            return render_template('login.html', error="Invalid username or password")
     else:
        request.method == 'GET'
        return render_template('login.html')
@app.route('/registrationform', methods=['POST', 'GET'])

def registrationform():
    brawlStarsMapTrackerRegistrationForm=BrawlStarsMapTrackerRegistrationForm()
    con=sqlite3.connect('user1.db')
    c=con.cursor()
    if request.method=='POST':
        if(request.form["name"]!="" and request.form["passWord"]!=""):
            name=request.form["name"]
            passWord=request.form["passWord"]
            statement=f"SELECT * from user1 WHERE name='{name}' AND passWord='{passWord}';"
            c.execute(statement)
            data=c.fetchone()
            if data:
                return render_template("error.html")
            else:
                if not data:
                    c.execute("INSERT INTO user1 (name,passWord) VALUES (?,?)",(name,passWord))
                    con.commit()
                    con.close()
                return render_template('successformsubmission.html')
    elif request.method=='GET':
        return render_template('register.html', form=brawlStarsMapTrackerRegistrationForm)
      
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/successformsubmission')
def successformsubmission():
    name=session.get('name', None)
    return render_template('successformsubmission.html')

def notify():
    active_map_names = fetch_active_map_names()
    notify_users(active_map_names)

# scheduler.add_job(func=notify, trigger='interval', seconds = 120, id='notifs')
# scheduler.start()
# app.run(debug=True)


#email app password: hxqg qban uwxu spns
