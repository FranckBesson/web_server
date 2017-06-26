# coding=utf-8

from db import Db
import json

db = Db()
# ========================== playerinfo ==========================
# Requête pour lister les items des joueur
def get_player_info():
  playerInfo = {}

  db_player_response = db.select("""
      SELECT *
      FROM player;
    """)

  # Player by player
  #for player in db_player_response :
    #onPlayerInfo = {
    #  "cash" : player["player_budget"],
    #  "sales" : ,
    #  "profit" : ,
    #  "drinksOffered" :
    #}

    #playerInfo[player["player_name"]] = onPlayerInfo

  return playerInfo

# ========================== itemsByPlayer ==========================
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

  # Liste de items d'un joueur
  items = []

    items.append(item)

  return db_item_possession_response

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


def players_post_request(elements):
  	response = {
  	  "name" : elements["name"],
  	  "location" : get_player_location_by_player_name(elements["name"]),
  	  "info" : None
  	}
	return json.dumps(response), 200, { "Content-Type": "application/json" }