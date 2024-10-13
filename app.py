from flask import Flask, render_template
import requests
import json 
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Brawl Stars Map Tracker")

res = requests.get('https://api.brawlify.com/v1/events')
response = json.loads(res.text)
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
mapName6 = response['active'][8]['map']['name']
mapMode6 = response['active'][8]['map']['gameMode']['name']
print(mapMode6 + ": " + mapName6);