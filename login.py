from flask import Flask, render_template
from cs50 import SQL
db=SQL("sqlite:///data.db")
app = Flask(__name__)
app.secret_key="__privatekey__"

@app.route('/')
def defaultHome():
    return render_template('home.html')

db.execute("""
    CREATE TABLE IF NOT EXISTS user1 (
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST','GET'])
def login():

@app.route('/registrationform', methods=['POST', 'GET'])
def registrationform():