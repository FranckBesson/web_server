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

  # Requête pour connaitre le jour actuel
  db_time_response = db.select("\
      SELECT * FROM time;\
    ")
  timestamp = (int)(db_time_response[0]["time_hour"])
  # Log
  print("-- log -- current timestamp : "+str(timestamp))
  current_day_number = (int)(timestamp/24)
  print("-- log -- current day number : "+str(current_day_number))

  # Ce tableau contiendra tout les objet "weather"
  weathers = []

  # On récupère le jour actuel
  db_current_weather_response = db.select("\
      SELECT day_weather FROM day\
      WHERE day_number = "+str(current_day_number)+";\
    ")

  # On test pour voir si le jour actuel est en base de donnée
  if len(db_current_weather_response) == 1 :

    print("-- log -- current day weather : "+str(db_current_weather_response[0]["day_weather"]))

    # On crée une map weather_today
    weather_today = {
      "dfn" : 0,
      "weather" : str(db_current_weather_response[0]["day_weather"])
    }

    # On l'ajoute à la liste
    weathers.append(weather_today)

  # On récupère le jour de demain
  db_tomorrow_weather_response = db.select("\
      SELECT day_weather FROM day\
      WHERE day_number = "+str(current_day_number+1)+";\
    ")

  # On test pour voir si le jour de demain est en base de donnée
  if len(db_tomorrow_weather_response) == 1 :

    print("-- log -- tomorrow day weather : "+str(db_tomorrow_weather_response[0]["day_weather"]))

    # On crée une map weather_tomorrow
    weather_tomorrow = {
      "dfn" : 1,
      "weather" : str(db_tomorrow_weather_response[0]["day_weather"])
    }

    # On l'ajoute à la liste
    weathers.append(weather_tomorrow)

  #Création de l'objet à renvoyer
  response = {
    "timestamp" : timestamp,
    "weather" : weathers
  }

  # Log
  print("-- log -- response : "+str(response))

  db.close()
  
  return json_response(response)

# R2 Obtenir les détails d'une partie
# Par le simulateur Java
@app.route("/map", methods=['GET'])
def map_get():
  
  db = Db()

  # ========================== Region ==========================
  # Requête pour connaitre lse infomrations de la map
  db_map_response = db.select("\
      SELECT * FROM map;\
    ")

  # Récupération des information sur celle-ci
  map_center_x = (float)(db_map_response[0]["map_center_x"])
  map_center_y = (float)(db_map_response[0]["map_center_y"])
  map_span_x = (float)(db_map_response[0]["map_span_x"])
  map_span_y = (float)(db_map_response[0]["map_span_y"])

  # On créer une map pour formater ces données
  coordinates = {
    "latitude" : map_center_x,
    "longitude" : map_center_y
  }
  coordinatesSpan = {
    "latitudeSpan" : map_span_x,
    "longitudeSpan" : map_span_y
  }
  region = {
    "center" : coordinates,
    "span" : coordinatesSpan
  }

  # ========================== Ranking ==========================
  # Requête pour lister les joueur du plus riche au moins riche
  # !!!!!!!!!!!! Bug ici on ne nous retourne pas tout !
  db_player_rank_response = db.select("\
      SELECT player_name , RANK() OVER(ORDER BY PLAYER_BUDGET DESC) AS rank\
      FROM player;\
    ")

  # Création d'un tableau pour placer les joueur par ordre de richesse
  ranking = []

  print("-- log -- " + str(db_player_rank_response))

  # Itération sur la réponse pour alimenter le tableau
  for player in db_player_rank_response :
    print("-- log -- " + str(player))
    #ranking.append(player["player_name"])

  # ========================== itemsByPlayer ==========================
  # Requête pour lister les items des joueur

  db_player_response = db.select("\
      SELECT player_id, player_name\
      FROM player;\
    ")
  
  # Player by player
  for player in db_player_response :

    db_item_possession_response = db.select("\
        SELECT item_possession_item_id\
        FROM item_possession\
        WHERE item_possession_player_id = '"+str(player["player_id"])+"';\
      ")
    # Item of player by item of player
    for item in db_item_possession_response :

      db_item_possession_response = db.select("\
        SELECT *\
        FROM item\
        WHERE item_id = '"+str(item["item_possession_item_id"])+"';\
      ")

      coordinates = {
        "latitude" : db_item_possession_response["item_x_coordinate"],
        "longitude" : db_item_possession_response["item_y_coordinate"]
      }

      mapItem = {
        "kind" : db_item_possession_response["item_kind"],
        "owner" : player["player_name"],
        "location" : coordinates,
        "influence" : db_item_possession_response["item_influence"]
      }

      print(str(mapItem))

  db.close()

  

  

  # C'est la merde là
  itemsByPlayer = {

  }

  # C'est la merde là
  playerInfo = {

  }

  # C'est la merde là
  drinksByPlayer = {

  }

  # Création de la map _map
  _map = {
    "region" : region,
    "ranking" : ranking,
    "itemsByPlayer" : itemsByPlayer,
    "playerInfo" : playerInfo,
    "drinksByPlayer" : drinksByPlayer
  }

  #Création de l'objet à renvoyer
  response = {
    "map" : _map
  }

  return json_response(response)

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
