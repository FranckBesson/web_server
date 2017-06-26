# coding=utf-8

from db import Db
import json

db = Db()
# ========================== Region ==========================
# Requête pour connaitre lse infomrations de la map

def get_region():
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

  return region

# ========================== Ranking ==========================
# Requête pour lister les joueur du plus riche au moins riche

def get_ranking():
  
  db_player_rank_response = db.select("\
      SELECT player_name , RANK() OVER(ORDER BY PLAYER_BUDGET DESC) AS rank\
      FROM player;\
    ")

  # Création d'un tableau pour placer les joueur par ordre de richesse
  ranking = []

  print("-- log -- " + str(db_player_rank_response))

  # Itération sur la réponse pour alimenter le tableau
  for player in db_player_rank_response :
    print("-- log -- player :" + str(player))
    ranking.append(player["player_name"])

  return ranking

# ========================== itemsByPlayer ==========================
# Requête pour lister les items des joueur
def get_item_by_player():

  itemsByPlayer = {}

  db_player_response = db.select("""
      SELECT player_id, player_name
      FROM player;
    """)
  print("-- log -- db_player_response : "+str(db_player_response))

  # Player by player
  for player in db_player_response :

    db_item_possession_response = db.select("\
        SELECT item_possession_item_id\
        FROM item_possession\
        WHERE item_possession_player_id = '"+str(player["player_id"])+"';\
      ")
    print("-- log -- player : "+str(db_item_possession_response))

    # Liste de items d'un joueur
    items = []

    # Item of player by item of player
    for item in db_item_possession_response :

      print("-- log -- item : "+str(item))

      db_item_possession_response = db.select("\
        SELECT *\
        FROM item\
        WHERE item_id = '"+str(item["item_possession_item_id"])+"';\
      ")

      coordinates = {
        "latitude" : db_item_possession_response[0]["item_x_coordinate"],
        "longitude" : db_item_possession_response[0]["item_y_coordinate"]
      }

      mapItem = {
        "kind" : db_item_possession_response[0]["item_kind"],
        "owner" : player["player_name"],
        "location" : coordinates,
        "influence" : db_item_possession_response[0]["item_influence"]
      }

      print("-- log -- mapItem : "+str(mapItem))
      items.append(mapItem)

    itemsByPlayer[str(player["player_name"])] = items

  return itemsByPlayer

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

def get_drinks_by_player():
  drinksByPlayer = {

  }

  return drinksByPlayer;

def map_get_request():

  # Récupération des valeurs
  region = get_region()
  ranking = get_ranking() 
  itemsByPlayer = get_item_by_player()
  playerinfo = get_player_info()
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