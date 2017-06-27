# coding=utf-8

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from db import Db
import json

from metrology_get import metrology_get_request
from map_get import map_get_request
from sales_post import sales_post_request
from players_post import players_post_request
from map_playername_get import map_playername_get_request
from actions_playername_post import actions_playername_post_request
from metrology_post import metrology_post_request
from reset_get import reset_get_request
from ingredients_get import ingredients_get_request

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
  return metrology_get_request()

# R2 Obtenir les détails d'une partie
# Par le simulateur Java
@app.route("/map", methods=['GET'])
def map_get():
  return map_get_request()
  

# R3 Commande "simulateur"
# Par le simulateur Java
@app.route("/sales", methods=['POST'])
def sales_post():
  return sales_post_request(request.get_json())

# R4 Quitter/Rejoindre une partie
# Par client web
@app.route("/players", methods=['POST'])
def players_post():
  #return players_post_request(request.get_json())
  return ""

# R5 Obtenir les détails d'une parie
# Par le client web
@app.route("/map/<playerName>", methods=['GET'])
def map_playername_get(playerName):
  return map_playername_get_request()

# R6 Instruction du joueur pour le jour suivant
# Par le client web
@app.route("/actions/<playerName>", methods=['POST'])
def actions_playername_post(playerName):
  return actions_playername_post_request(request.get_json(), playerName)

# R7 Commande temps (POST)
# Par le programme c
@app.route("/metrology", methods=['POST'])
def metrology_post():
  return metrology_post_request(request.get_json())

# R8 Réinitialiser une partie (GET)
# Par le client web
@app.route("/reset", methods=['GET'])
def reset_get():
  return reset_get_request()

# R9 Obtenir la liste des ingrédients
# Par le client web
@app.route("/ingredients", methods=['GET'])
def ingredients_get():
  # return ingredients_get_request()
  return ""

if __name__ == "__main__" :
   app.run()
