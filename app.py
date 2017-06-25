from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from db import Db
import json

app = Flask(__name__)
app.debug = True
CORS(app)

# For parsing json in request
def json_response(data="OK", status=200):
  return json.dumps(data), status, { "Content-Type": "application/json" }

# R1 Commande temps (GET)
# Par le client web et le simulateur java
@app.route("/metrology", methods=['GET'])
def metrology_get():
  
  db = Db()

  db_time_response = db.select("\
      SELECT * FROM time;\
    ")
  timestamp = (int)(db_time_response[0]["time_hour"])
  print("-- log -- current timestamp : "+str(timestamp))
  current_day_number = (int)(timestamp/24)
  print("-- log -- current day number : "+str(current_day_number))

  # Ce tableau contiendra tout les objet "weather"
  weathers = []

  db_current_weather_response = db.select("\
      SELECT day_weather FROM day\
      WHERE day_number = "+str(current_day_number)+";\
    ")
  
  if len(db_current_weather_response) == 1 :

    print("-- log -- current day weather : "+str(db_current_weather_response[0]["day_weather"]))

    weather_today = {
      "dfn" : 0,
      "weather" : str(db_current_weather_response[0]["day_weather"])
    }

    weathers.append(weather_today)

  db_tomorrow_weather_response = db.select("\
      SELECT day_weather FROM day\
      WHERE day_number = "+str(current_day_number+1)+";\
    ")

  if len(db_tomorrow_weather_response) == 1 :

    print("-- log -- tomorrow day weather : "+str(db_tomorrow_weather_response[0]["day_weather"]))

    weather_tomorrow = {
      "dfn" : 0,
      "weather" : str(db_tomorrow_weather_response[0]["day_weather"])
    }

    weathers.append(weather_tomorrow)

  time = {
    "timestamp" : timestamp,
    "weather" : weathers
  }

  print("-- log -- response : "+str(time))

  db.close()
  
  return jsonify(json.loads(open('exemple1.json').read()))

# R2 Obtenir les détails d'une partie
# Par le simulateur Java
@app.route("/map", methods=['GET'])
def map_get():
  return jsonify(json.loads(open('exemple2.json').read()))

# R3 Commande "simulateur"
# Par le simulateur Java
@app.route("/sales", methods=['POST'])
def sales_post():
  elements = request.get_json()
  print(str(elements))
  return json_response(elements)

# R4 Quitter/Rejoindre une partie
# Par client web
@app.route("/players", methods=['POST'])
def players_post():
  elements = request.get_json()
  print(str(elements))
  return jsonify(json.loads(open('exemple4.json').read()))

# R5 Obtenir les détails d'une parie
# Par le client web
@app.route("/map/<playerName>", methods=['GET'])
def map_playername_get(playerName):
  print(str(playerName))
  return jsonify(json.loads(open('exemple5.json').read()))

# R6 Instruction du joueur pour le jour suivant
# Par le client web
@app.route("/actions/<playerName>", methods=['POST'])
def actions_playername_post(playerName):
  elements = request.get_json()
  print(str(playerName))
  print(str(elements))

  return jsonify(json.loads(open('exemple6.json').read()))

# R7 Commande temps (POST)
# Par le programme c
@app.route("/metrology", methods=['POST'])
def metrology_post():
  elements = request.get_json()

  print("-- log -- elements : " + str(elements))
  print("-- log -- timestamp : " + str(elements["timestamp"]))
  weather = str(elements["weather"]["weather"])
  print("-- log -- weather : " + weather)

  db = Db()

  jour_actuel = (int)((int)(elements["timestamp"])/24)
  print(str(jour_actuel))

  
  # Jour courrant
  if elements["weather"]["dfn"] == "0" :

    print("current day")

    row = db.select("\
      SELECT * FROM DAY\
      WHERE DAY_NUMBER = "+str(jour_actuel)+";\
    ")

    print(str(row))

    if len(row) == 0 :

      db.execute("\
        INSERT INTO DAY\
        VALUES("+str(jour_actuel)+",\'"+str(weather)+"\');\
      ")

    else :

      db.execute("\
        UPDATE DAY SET DAY_WEATHER = \'"+str(weather)+"\'\
        WHERE DAY_NUMBER = "+str(jour_actuel)+";\
      ")

  # Jour suivant
  elif elements["weather"]["dfn"] == "1" :

    print("day after")

    row = db.select("\
      SELECT * FROM DAY\
      WHERE DAY_NUMBER = "+str(jour_actuel+1)+";\
    ")

    print(str(row))

    if len(row) == 0 :

      db.execute("\
        INSERT INTO DAY\
        VALUES("+str(jour_actuel+1)+",\'"+str(weather)+"\');\
      ")

    else :

      db.execute("\
        UPDATE DAY SET DAY_WEATHER = \'"+str(weather)+"\'\
        WHERE DAY_NUMBER = "+str(jour_actuel+1)+";\
      ")

  #Sauvegarde du timestamp
  db.execute("\
        DELETE FROM TIME;\
      ")

  db.execute("\
        INSERT INTO TIME\
        VALUES("+str(elements["timestamp"])+");\
      ")

  db.close()

  return json_response()

# R8 Réinitialiser une partie (GET)
# Par le client web
@app.route("/reset", methods=['GET'])
def reset_get():
  return json_response()

# R9 Obtenir la liste des ingrédients
# Par le client web
@app.route("/ingredients", methods=['GET'])
def ingredients_get():
  return jsonify(json.loads(open('exemple9.json').read()))

if __name__ == "__main__" :
   app.run()
