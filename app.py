from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
app.debug = True
CORS(app)

# For parsing json in request
def json_response(data="OK", status=200):
  return json.dumps(data), status, { "Content-Type": "application/json" }

# R1 Commande temps (GET)
@app.route("/metrology", methods=['GET'])
def metrology_get():
  return jsonify(json.loads(open('exemple1.json').read()))

# R2 Obtenir les détails d'une partie
@app.route("/map", methods=['GET'])
def map_get():
  return jsonify(json.loads(open('exemple2.json').read()))

# R3 Commande "simulateur"
@app.route("/sales", methods=['POST'])
def sales_post():
  elements = request.get_json()
  print(str(elements))
  return json_response(elements)

# R4 Quitter/Rejoindre une partie
@app.route("/players", methods=['POST'])
def players_post():
  elements = request.get_json()
  print(str(elements))
  return jsonify(json.loads(open('exemple4.json').read()))

# R5 Obtenir les détails d'une parie
@app.route("/map/<playerName>", methods=['GET'])
def map_playername_get(playerName):
  print(str(playerName))
  return jsonify(json.loads(open('exemple5.json').read()))

# R6 INstruction du joueur pour le jour suivant
@app.route("/actions/<playerName>", methods=['POST'])
def actions_playername_post():
  elements = request.get_json()
  return json_response(elements)

# R7 Commande temps (POST)
@app.route("/metrology", methods=['POST'])
def metrology_post():
  elements = request.get_json()
  return json_response(elements)

# R8 Réinitialiser une partie (GET)
@app.route("/reset", methods=['POST'])
def reset_get():
  elements = request.get_json()
  return json_response(elements)

# R9 Obtenir la liste des ingrédients
@app.route("/ingredients", methods=['GET'])
def ingredients_get():
  return jsonify(json.loads(open('exemple9.json').read()))

if __name__ == "__main__" :
   app.run()
