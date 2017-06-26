# coding=utf-8

from db import Db
import json

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

def get_player_location_by_player_name(player_name):
	
	items = get_items_by_player_name(player_name)

	print("0")

	for item in items :

		print("1")

		if item["item_kind"] == "STAND" :

			print("2")

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

# ========================== create_player_by_name ==========================
# Créer un joueur
def create_player_by_name(player_name):

	db.execute("""
		INSERT INTO player(player_budget, player_influence, player_name)
		VALUES("""+str(10)+""","""+str(1)+""",'"""+str(player_name)+"""');
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