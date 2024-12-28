from flask import Flask, flash, render_template, request, session, redirect, url_for
import requests
import json 
#https://cs50.readthedocs.io/libraries/cs50/python/
from cs50 import SQL
import sqlite3
from formsubmission import BrawlStarsMapTrackerRegistrationForm
#db=SQL("sqlite:///data.db")
app = Flask(__name__)
app.secret_key="__privatekey__"

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
    
active_map_names = fetch_active_map_names()
print("Active maps:", active_map_names)

def create_table():
    con = sqlite3.connect('user1.db')
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user1(name text, passWord text)")
    c.execute("CREATE TABLE IF NOT EXISTS currentMaps(map_name text)")
    c.execute("CREATE TABLE IF NOT EXISTS favoriteMaps(user_name text, map_name text)")
    con.commit()
    con.close()

create_table()

@app.route('/home', methods=['POST','GET'])
def home():
        if 'username' not in session:
             return redirect('/login')
        username = session['username']
        print(f"User logged in: {username}")
        brawlStarsMapTrackerRegistrationForm=BrawlStarsMapTrackerRegistrationForm()
        return render_template('index.html',form=brawlStarsMapTrackerRegistrationForm)
        


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

# def hello_world():
#     return render_template("index.html", title="Brawl Stars Map Tracker", 
#                            mapName1a=mapName1a, mapMode1a=mapMode1a,
#                            mapName1b=mapName1b, mapMode1b=mapMode1b, 
#                            mapName2=mapName2, mapMode2=mapMode2,
#                            mapName3=mapName3, mapMode3=mapMode3,
#                            mapName4=mapName4, mapMode4=mapMode4,
#                            mapName5=mapName5, mapMode5=mapMode5,
#                            mapName6=mapName6, mapMode6=mapMode6,
#                            mapName7=mapName7, mapMode7=mapMode7)
#                            mapName8=mapName8, mapMode8=mapMode8,
#                            mapName9=mapName9, mapMode9=mapMode9

# mapName1a = response['active'][0]['map']['name']
# mapMode1a = response['active'][0]['map']['gameMode']['name']
# print(mapMode1a + ": " + mapName1a);
# mapName1b = response['active'][1]['map']['name']
# mapMode1b = response['active'][1]['map']['gameMode']['name']
# print(mapMode1b + ": " + mapName1b);
# mapName2 = response['active'][2]['map']['name']
# mapMode2 = response['active'][2]['map']['gameMode']['name']
# print(mapMode2 + ": " + mapName2);
# mapName3 = response['active'][3]['map']['name']
# mapMode3 = response['active'][3]['map']['gameMode']['name']
# print(mapMode3 + ": " + mapName3);
# mapName4 = response['active'][4]['map']['name']
# mapMode4 = response['active'][4]['map']['gameMode']['name']
# print(mapMode4 + ": " + mapName4);
# mapName5 = response['active'][5]['map']['name']
# mapMode5 = response['active'][5]['map']['gameMode']['name']
# print(mapMode5 + ": " + mapName5);
# mapName6 = response['active'][6]['map']['name']
# mapMode6 = response['active'][6]['map']['gameMode']['name']
# print(mapMode6 + ": " + mapName6);
# mapName7 = response['active'][7]['map']['name']
# mapMode7 = response['active'][7]['map']['gameMode']['name']
# print(mapMode7 + ": " + mapName7);