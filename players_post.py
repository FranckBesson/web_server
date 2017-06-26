# coding=utf-8

from db import Db
import json
import random

db = Db()


# ========================== get_player_sale_by_player_name ==========================
# Récupère les vente d'un joueur
def get_player_sale_by_player_name(player_name):
  db_player_response = db.select("""
      SELECT *
      FROM player
      WHERE player_name = '"""+player_name+"""';
    """)

  player_sale = {}

  return player_sale

# ========================== get_player_profit_by_player_name ==========================
# Récupère le profit d'un joueur
def get_player_profit_by_player_name(player_name):
  db_player_response = db.select("""
      SELECT *
      FROM player
      WHERE player_name = '"""+player_name+"""';
    """)

  player_profit = {}

  return player_profit

# ========================== get_player_drinks_offered_by_player_name ==========================
# Récupère les boissons proposées d'un joueur
def get_player_drinks_offered_by_player_name(player_name):
  db_player_response = db.select("""
      SELECT *
      FROM player
      WHERE player_name = '"""+player_name+"""';
    """)

  player_drinks_offered = {}

  return player_drinks_offered

# ========================== get_player_info_by_player_name ==========================
# Requête pour lister les items des joueur
def get_player_info_by_player_name(player_name):

  db_player_response = db.select("""
      SELECT *
      FROM player
      WHERE player_name = '"""+player_name+"""';
    """)
  player = db_player_response[0]

  playerInfo = {
    "cash" : player["player_budget"],
    "sales" : get_player_sale_by_player_name(player_name),
    "profit" : get_player_profit_by_player_name(player_name),
    "drinksOffered" : get_player_drinks_offered_by_player_name(player_name)
  }

  return playerInfo

# ========================== get_items_by_player_name ==========================
# Requête pour lister les items des joueur
def get_items_by_player_name(player_name):

  db_player_response = db.select("""
      SELECT *
      FROM player
      WHERE player_name = '"""+str(player_name)+"""';
    """)

  db_item_possession_response = db.select("\
      SELECT item_possession_item_id\
      FROM item_possession\
      WHERE item_possession_player_id = '"+str(db_player_response[0]["player_id"])+"';\
    ")

  return db_item_possession_response

# ========================== get_player_location_by_player_name ==========================
# Récupère la position par player_name
def get_player_location_by_player_name(player_name):
	
	items = get_items_by_player_name(player_name)

	for item in items :

		if item["item_kind"] == "STAND" :

			location = {
			  "latitude" : item["item_x_coordinate"],
			  "longitude" : item["item_y_coordinate"]
			}

	        return location

	return None

# ========================== player_exist ==========================
# Requête pour lister les items des joueur
def player_exist(player_name):

  db_player_response = db.select("""
      SELECT *
      FROM player
      WHERE player_name = '"""+str(player_name)+"""';
    """)

  if len(db_player_response) != 0 :

  	return True

  else :

  	return False

# ========================== get_new_location ==========================
# renvoie une nouvelle coordée dans la map qui n'est pas déjà attribuée
def get_new_location():

  # db_item_response = db.select("""
  #   SELECT item_x_coordinate, item_y_coordinate
  #   FROM item;
  # """)

  db_map_response = db.select("""
    SELECT *
    FROM map;
  """)

  span_x = db_map_response[0]["map_span_x"]
  span_y = db_map_response[0]["map_span_y"]

  x_rand = random.random() * span_x
  y_rand = random.random() * span_y

  location = {
  	"latitude" : x_rand,
  	"longitude" : y_rand
  }

  return location

# ========================== create_player_by_name ==========================
# Créer un joueur
def create_player_by_name(player_name):

	db.execute("""
		INSERT INTO player(player_budget, player_influence, player_name)
		VALUES("""+str(10)+""","""+str(1)+""",'"""+str(player_name)+"""');
		""")

	location = get_new_location()
	print(str(location))

	db.execute("""
		INSERT INTO item(item_kind, item_influence, item_x_coordinate, item_y_coordinate)
		VALUES('STAND', 1,"""+str(location["item_x_coordinate"])+""", """+str(location["item_y_coordinate"])+""");
		""")

# ========================== players_post_request ==========================
# Requête pour log un utilisateur
def players_post_request(elements):

  name = str(elements["name"])

  if player_exist(name) == False :

    create_player_by_name(name)

  response = {
    "name" : name,
    "location" : get_player_location_by_player_name(name),
    "info" : get_player_info_by_player_name(name)
  }

  return json.dumps(response), 200, { "Content-Type": "application/json" }