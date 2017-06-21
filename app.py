from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
app.debug = True
CORS(app)

# R1 Commande temps (GET)
@app.route("/metrology", methods=['GET'])
def metrology_get():
  return "metrology_get"

# R2 Obtenir les détails d'une partie
@app.route("/map", methods=['GET'])
def map_get():
  return "map_get"

# R3 Commande "simulateur"
@app.route("/sales", methods=['POST'])
def sales_post():
  return "sales_post"

# R4 Quitter/Rejoindre une partie
@app.route("/players", methods=['POST'])
def players_post():
  return "player_post" 

# R5 Obtenir les détails d'une parie
@app.route("/map/<playerName>", methods=['GET'])
def map_playername_get():
  return "map_playername_get"

# R6 INstruction du joueur pour le jour suivant
@app.route("/actions/<playerName>", methods=['POST'])
def actions_playername_post():
  return "actions_playername_post"

# R7 Commande temps (POST)
@app.route("/metrology", methods=['POST'])
def metrology_post():
  return "metrology_post"

# R8 Réinitialiser une partie (GET)
@app.route("/reset", methods=['POST'])
def reset_get():
  return "reset_get"

# R9 Obtenir la liste des ingrédients
@app.route("/ingredients", methods=['GET'])
def ingredients_get():
  return "ingredients_get"

if __name__ == "__main__" :
   app.run()
