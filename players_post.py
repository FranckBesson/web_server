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

# ========================== get_recipe_produce_price_by_name ==========================
# Calcule le prix de production d'une recette
def get_recipe_produce_price_by_name(recipe_name):
	db_recipe_compose_response = db.select("""
		SELECT compose_ingredient_recipe_name
		FROM compose
		WHERE compose_recipe_name = '"""+recipe_name+"""';
		""")

	cumule = 0

	for recipe in db_recipe_possession_response :

		db_recipe_response = db.select("""
			SELECT recipe_price
			FROM recipe
			WHERE recipe_name = '"""+recipe["compose_ingredient_recipe_name"]+"""';
			""")

		cumule += (float)(db_recipe_response["recipe_price"])

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
