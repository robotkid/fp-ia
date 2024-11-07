from flask import Flask, render_template
import requests
import json 
#https://cs50.readthedocs.io/libraries/cs50/python/
from cs50 import SQL
from formsubmission import BrawlStarsMapTrackerRegistrationForm
db=SQL("sqlite:///data.db")
#app = Flask(__name__)
#app.secret_key="__privatekey__"

res = requests.get('https://api.brawlify.com/v1/events')
response = json.loads(res.text)

#https://stackoverflow.com/questions/31270488/navigating-json-in-python

mapName1a = response['active'][0]['map']['name']
mapMode1a = response['active'][0]['map']['gameMode']['name']
print(mapMode1a + ": " + mapName1a);
mapName1b = response['active'][1]['map']['name']
mapMode1b = response['active'][1]['map']['gameMode']['name']
print(mapMode1b + ": " + mapName1b);
mapName2 = response['active'][2]['map']['name']
mapMode2 = response['active'][2]['map']['gameMode']['name']
print(mapMode2 + ": " + mapName2);
mapName3 = response['active'][3]['map']['name']
mapMode3 = response['active'][3]['map']['gameMode']['name']
print(mapMode3 + ": " + mapName3);
mapName4 = response['active'][4]['map']['name']
mapMode4 = response['active'][4]['map']['gameMode']['name']
print(mapMode4 + ": " + mapName4);
mapName5 = response['active'][5]['map']['name']
mapMode5 = response['active'][5]['map']['gameMode']['name']
print(mapMode5 + ": " + mapName5);
mapName6 = response['active'][6]['map']['name']
mapMode6 = response['active'][6]['map']['gameMode']['name']
print(mapMode6 + ": " + mapName6);
mapName7 = response['active'][7]['map']['name']
mapMode7 = response['active'][7]['map']['gameMode']['name']
print(mapMode7 + ": " + mapName7);
mapName8 = response['active'][8]['map']['name']
mapMode8 = response['active'][8]['map']['gameMode']['name']
print(mapMode8 + ": " + mapName8);
mapName9 = response['active'][9]['map']['name']
mapMode9 = response['active'][9]['map']['gameMode']['name']
print(mapMode9 + ": " + mapName9);

#source - https://stackoverflow.com/questions/68429566/how-to-return-render-template-in-flask
#names are default because I just added on to the one which already existed for the title
@app.route("/")
def hello_world():
    return render_template("index.html", title="Brawl Stars Map Tracker", 
                           mapName1a=mapName1a, mapMode1a=mapMode1a,
                           mapName1b=mapName1b, mapMode1b=mapMode1b, 
                           mapName2=mapName2, mapMode2=mapMode2,
                           mapName3=mapName3, mapMode3=mapMode3,
                           mapName4=mapName4, mapMode4=mapMode4,
                           mapName5=mapName5, mapMode5=mapMode5,
                           mapName6=mapName6, mapMode6=mapMode6,
                           mapName7=mapName7, mapMode7=mapMode7,
                           mapName8=mapName8, mapMode8=mapMode8,
                           mapName9=mapName9, mapMode9=mapMode9)
