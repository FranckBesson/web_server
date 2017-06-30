# coding=utf-8

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from db import Db
from api import *
import json

db = Db()

app = Flask(__name__)
app.debug = True
CORS(app)

# R1 Commande temps (GET)
# Par le client web et le simulateur java
@app.route("/metrology", methods=['GET'])
def metrology_get():

  weathers = []

  # On récupère le jour actuel
  weather_today = get_weather_today()

  if weather_today != False :

    weathers.append(weather_today)

  # On récupère le jour de demain
  weather_tomorrow = get_weather_tomorrow()

  if weather_tomorrow != False :

    weathers.append(weather_tomorrow)

  #Création de l'objet à renvoyer
  response = {
    "timestamp" : get_timestamp(),
    "weather" : weathers
  }
  
  return json.dumps(response), 200, { "Content-Type": "application/json" }

# R2 Obtenir les détails d'une partie
# Par le simulateur Java
@app.route("/map", methods=['GET'])
def map_get():

  # Récupération des valeurs
  region = get_region()
  ranking = get_ranking() 
  itemsByPlayer = get_item_by_player()
  playerinfo = get_player_info_R2()
  drinksByPlayer = get_drinks_by_player()

  # Création de la map _map
  _map = {
    "region" : region,
    "ranking" : ranking,
    "itemsByPlayer" : itemsByPlayer,
    "playerInfo" : playerinfo,
    "drinksByPlayer" : drinksByPlayer
  }

  #Création de l'objet à renvoyer
  response = {
    "map" : _map
  }

  return json.dumps(response), 200, { "Content-Type": "application/json" }
  
# R3 Commande "simulateur"
# Par le simulateur Java
@app.route("/sales", methods=['POST'])
def sales_post():

  elements = request.get_json()

  sales = elements["sales"]

  for sale in sales :

    current_day = get_current_day_number()

    # On caste la valeur de quantity pour pas que le joueur ne vende plus de boisson
    new_quantity = cast_quantity_value_for_sale(float(sale["quantity"]),current_day,str(sale["item"]),str(sale["player"]))

    # Mise à jour de la table sale pour prendre en compte les ventes
    db.execute("""
      UPDATE SALE
      SET sale_number = """+str(new_quantity)+"""
      WHERE sale_day_number = """+str(current_day)+"""
      AND sale_recipe_name = '"""+str(sale["item"])+"""'
      AND sale_player_name = '"""+str(sale["player"])+"""';
    """)

  # Effectue une mise à jour du budget de tout les joueurs
  calculate_all_sales()

  return json.dumps(""), 200, { "Content-Type": "application/json" }  

# R4 Quitter/Rejoindre une partie
# Par client web
@app.route("/players", methods=['POST'])
def players_post():

  elements = request.get_json()

  name = str(elements["name"])

  if player_exist(name) == False :

    create_player_by_name(name)

  response = {
    "name" : name,
    "location" : get_player_location_by_player_name(name),
    "info" : get_player_info_R5_by_player_name(name)
  }

  return json.dumps(response), 200, { "Content-Type": "application/json" }

# R5 Obtenir les détails d'une partie
# Par le client web
@app.route("/map/<playerName>", methods=['GET'])
def map_playername_get(playerName):

  _map = {
    "region" : get_region(),
    "ranking" : get_ranking() ,
    "itemsByPlayer" : get_item_by_player()
  }

  response = {
    "availableIngredients" : get_available_ingredients(playerName),
    "map" : _map,
    "playerInfo" : get_player_info_R5_by_player_name(playerName)
  }

  return json.dumps(response), 200, { "Content-Type": "application/json" }

# R6 Instruction du joueur pour le jour suivant
# Par le client web
@app.route("/actions/<playerName>", methods=['POST'])
def actions_playername_post(playerName):

    elements = request.get_json()

    player_actions = elements["actions"]
    player_name = str(playerName)

    cost = 0.0

    for player_action in player_actions :
    
        if player_action["kind"] == "ad" :

            cost += float(player_action["radius"]) * 10.0

        elif player_action["kind"] == "drinks" :

            # Technique certainement gitanne et précaire mais d'apoint
            for key in player_action["prepare"]:

                sale_recipe_name = key
                sale_produce = player_action["prepare"][key]
    
                cost += float(sale_produce) * float(get_recipe_produce_price_by_name(str(sale_recipe_name)))

    if player_have_enough_budget_by_player_name(player_name, cost) :

        for player_action in player_actions :
        
            if player_action["kind"] == "recipe" :
        
                player_action_recipe(player_action,player_name)
                    
            elif player_action["kind"] == "ad" :
        
                player_action_ad(player_action,player_name)
    
            elif player_action["kind"] == "drinks" :
        
                player_action_drinks(player_action,player_name)

        response = {
            "sufficientFunds" : True,
            "totalCost" : cost
        }

        return json.dumps(response), 200, { "Content-Type": "application/json" }

    else :

        response = {
            "sufficientFunds" : False,
            "totalCost" : cost
        }

        return json.dumps(response), 200, { "Content-Type": "application/json" }

# R7 Commande temps (POST)
# Par le programme c
@app.route("/metrology", methods=['POST'])
def metrology_post():

  elements = request.get_json()

  forcast = elements["weather"]

  jour_actuel = (int)((int)(elements["timestamp"])/24)

  print(str("Day : "+str(jour_actuel)))

  for weather in forcast :

    # Jour courrant
    if weather["dfn"] == "0" :
  
      set_day_weather_where_day_number(jour_actuel,weather["weather"])
  
    # Jour suivant
    elif weather["dfn"] == "1" :
  
      set_day_weather_where_day_number(jour_actuel+1,weather["weather"])
         
    insert_new_timestamp(elements["timestamp"])

  return json.dumps(""), 200, { "Content-Type": "application/json" }

# R8 Réinitialiser une partie (GET)
# Par le client web
@app.route("/reset", methods=['GET'])
def reset_get():
  return reset_get_request()

# R9 Obtenir la liste des ingrédients
# Par le client web
@app.route("/ingredients", methods=['GET'])
def ingredients_get():

  return json.dumps(get_ingredients()), 200, { "Content-Type": "application/json" }

if __name__ == "__main__" :
   app.run()
