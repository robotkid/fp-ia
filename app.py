from flask import Flask, render_template
import requests
import json 
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Brawl Stars Map Tracker")

res = requests.get('https://api.brawlify.com/v1/events')
response = json.loads(res.text)
print(response)