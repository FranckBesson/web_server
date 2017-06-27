# coding=utf-8

from db import Db
import json
import random

db = Db()


# ========================== get_player_sale_by_player_name ==========================
# Récupère les vente d'un joueur
def get_player_sale_by_player_name(player_name):

  db_sale_player_response = db.select("""
      SELECT *
      FROM sale
      WHERE sale_player_name = '"""+player_name+"""';
    """)

  sales = 0

  for sale in db_sale_player_response :

  	sales += (int)(sale["sale_number"])

  return sales

# ========================== get_player_profit_by_player_name ==========================
# Récupère le profit d'un joueur
def get_player_profit_by_player_name(player_name):

  db_sale_player_response = db.select("""
      SELECT *
      FROM sale
      WHERE sale_player_name = '"""+player_name+"""';
    """)

  profit = 0.0

  for sale in db_sale_player_response :

  	# Récupère les données pour le calcul
  	sale_number = (int)(sale["sale_number"])
  	sale_produce = (int)(sale["sale_produce"])
  	sale_recipe_price = (float)(get_recipe_sale_price_by_name(sale["sale_recipe_name"]))
  	sale_recipe_produce_price = (float)(get_recipe_produce_price_by_name(sale["sale_recipe_name"]))

  	# Calcul le profit
  	profit += sale_number * sale_recipe_price - sale_produce * sale_recipe_produce_price

  return profit

# ========================== get_recipe_sale_price_by_name ==========================
# Retourne le prix d'achat d'une recette
def get_recipe_sale_price_by_name(recipe_name):

	db_recipe_compose_response = db.select("""
		SELECT recipe_price
		FROM recipe
		WHERE recipe_name = '"""+recipe_name+"""';
		""")

	if len(db_recipe_compose_response) == 1 :

		return db_recipe_compose_response[0]["recipe_price"]

	else :

		return None

# ========================== get_recipe_produce_price_by_name ==========================
# Calcule le prix de production d'une recette
def get_recipe_produce_price_by_name(recipe_name):
	
	db_recipe_compose_response = db.select("""
		SELECT compose_ingredient_recipe_name
		FROM compose
		WHERE compose_recipe_name = '"""+recipe_name+"""';
		""")

	cumule = 0

	for recipe in db_recipe_compose_response :

		db_recipe_response = db.select("""
			SELECT recipe_price
			FROM recipe
			WHERE recipe_name = '"""+recipe["compose_ingredient_recipe_name"]+"""';
			""")

		cumule += (float)(db_recipe_response[0]["recipe_price"])

	return cumule

# ========================== get_player_drinks_offered_by_player_name ==========================
# Récupère les boissons proposées d'un joueur
def get_player_drinks_offered_by_player_name(player_name):

  db_recipe_possession_response = db.select("""
      SELECT recipe_possession_recipe_name
      FROM recipe_possession
      WHERE recipe_possession_player_name = '"""+player_name+"""';
    """)

  # Formatage des données
  drinksOffered = []
  for recipe in db_recipe_possession_response :

    db_recipe_response = db.select("""
        SELECT *
        FROM recipe
        WHERE recipe_name = '"""+recipe["recipe_possession_recipe_name"]+"""';
      """)

    if len(db_recipe_response) == 1 :

      # For this we need the produce price !!!!!!
      drink_info = {
        "name" : db_recipe_response[0]["recipe_name"],
        "price" : get_recipe_produce_price_by_name(db_recipe_response[0]["recipe_name"]),
        "hasAlcohol" : db_recipe_response[0]["recipe_alcohol"],
        "isCold" : db_recipe_response[0]["recipe_cold"]
      }

      drinksOffered.append(drink_info)

  return drinksOffered

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

  db_items_by_player_response = db.select("""
      SELECT *
      FROM item
      WHERE item_owner = '"""+str(player_name)+"""';
    """)

  return db_item_possession_response

# ========================== get_player_location_by_player_name ==========================
# Récupère la position par player_name
def get_player_location_by_player_name(player_name):
	
  db_stand_response = db.select("\
      SELECT item_x_coordinate, item_y_coordinate\
      FROM item\
      WHERE item_owner = '"+str(player_name)+"' AND item_kind = 'STAND';\
    ")

  location = {
      "latitude" : None,
      "longitude" : None
  }

  if len(db_stand_response) == 1 :

    item = db_stand_response[0]

    location = {
      "latitude" : item["item_x_coordinate"],
      "longitude" : item["item_y_coordinate"]
    }

  return location

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

	# On créer son joueur
	db.execute("""
		INSERT INTO player(player_name, player_budget, player_influence)
		VALUES('"""+str(player_name)+"""',"""+str(10)+""","""+str(1)+""");
		""")

	location = get_new_location()

	# On lui attribue un stand placé au hasard
	db.execute("""
		INSERT INTO item(item_kind, item_influence, item_owner, item_x_coordinate, item_y_coordinate)
		VALUES('STAND', 1, '"""+str(player_name)+"""',"""+str(location["latitude"])+""", """+str(location["longitude"])+""");
		""")

	# On donne par défault la recette limonade
	db.execute("""
		INSERT INTO recipe_possession
		VALUES('"""+str(player_name)+"""','lemonade');
		""")

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
      SELECT player_name
      FROM player;
    """)

  # Player by player
  for player in db_player_response :

    db_item_response = db.select("""
        SELECT *
        FROM item
        WHERE item_owner = '"""+player["player_name"]+"""';
      """)

    # Liste de items d'un joueur
    items = []

    # Item of player by item of player
    for item in db_item_response :

      coordinates = {
        "latitude" : item["item_x_coordinate"],
        "longitude" : item["item_y_coordinate"]
      }

      mapItem = {
        "kind" : item["item_kind"],
        "owner" : player["player_name"],
        "location" : coordinates,
        "influence" : item["item_influence"]
      }

      items.append(mapItem)

    itemsByPlayer[str(player["player_name"])] = items

  return itemsByPlayer

# ========================== get_player_info ==========================
# Requête pour lister les info des joueurs
def get_player_info():

  playerInfo = {}

  db_player_response = db.select("""
    SELECT *
    FROM player;
  """)

  for player in db_player_response :

    playerInfo[player["player_name"]] = get_player_info_by_player_name(player["player_name"])

  return playerInfo

# ========================== get_drinks_by_player ==========================
# Requête pour lister les recette des joueurs
def get_drinks_by_player():
  drinksByPlayer = {}

  db_player_response = db.select("""
    SELECT *
    FROM player;
  """)

  for player in db_player_response :

    drinksByPlayer[player["player_name"]] = get_player_drinks_offered_by_player_name(player["player_name"])

  return drinksByPlayer;