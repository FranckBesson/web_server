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
# Récupère les boissons proposées d'un joueur pour le jour actuel (dans sale)
def get_player_drinks_offered_by_player_name(player_name):

  db_recipe_possession_response = db.select("""
      SELECT sale_recipe_name
      FROM sale
      WHERE sale_player_name = '"""+player_name+"""'
      AND sale_day_number = """+str(get_current_day_number())+""";
    """)

  # Formatage des données
  drinksOffered = []
  for recipe in db_recipe_possession_response :

    db_recipe_response = db.select("""
        SELECT *
        FROM recipe
        WHERE recipe_name = '"""+recipe["sale_recipe_name"]+"""';
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

# ========================== get_player_info_R2_by_player_name ==========================
# Requête pour lister les items des joueur
# PB de conception là ...
def get_player_info_R2_by_player_name(player_name):

  db_player_response = db.select("""
      SELECT *
      FROM player
      WHERE player_name = '"""+player_name+"""';
    """)

  if len(db_player_response) == 1 :

    player = db_player_response[0]

    playerInfo = {
      "cash" : player["player_budget"],
      "sales" : get_player_sale_by_player_name(player_name),
      "profit" : get_player_profit_by_player_name(player_name),
      "drinksOffered" : get_player_drinks_offered_by_player_name(player_name)
    }

    return playerInfo

  return None

# ========================== get_player_info_R5_by_player_name ==========================
# Requête pour lister les items des joueur
# PB de conception là ...
def get_player_info_R5_by_player_name(player_name):

  db_player_response = db.select("""
      SELECT *
      FROM player
      WHERE player_name = '"""+player_name+"""';
    """)

  if len(db_player_response) == 1 :

    player = db_player_response[0]

    playerInfo = {
      "cash" : player["player_budget"],
      "sales" : get_player_sale_by_player_name(player_name),
      "profit" : get_player_profit_by_player_name(player_name),
      "drinksOffered" : get_player_drinks_by_player_name(player_name)
    }

    return playerInfo

  return None



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

  # Itération sur la réponse pour alimenter le tableau
  for player in db_player_rank_response :
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

# ========================== get_player_info_R5 ==========================
# Requête pour lister les info des joueurs pour le client web
# Pb de conception des requêtes là ...
def get_player_info_R2():

  playerInfo = {}

  db_player_response = db.select("""
    SELECT *
    FROM player;
  """)

  for player in db_player_response :

    playerInfo[player["player_name"]] = get_player_info_R2_by_player_name(player["player_name"])

  return playerInfo

# ========================== get_player_info ==========================
# Requête pour lister les info des joueurs
# Pb de conception des requêtes là ...
def get_player_info_R5():

  playerInfo = {}

  db_player_response = db.select("""
    SELECT *
    FROM player;
  """)

  for player in db_player_response :

    playerInfo[player["player_name"]] = get_player_info_R5_by_player_name(player["player_name"])

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

    drinksByPlayer[player["player_name"]] = get_player_drinks_by_player_name(player["player_name"])

  return drinksByPlayer;


# ========================== get_player_drinks_by_player_name ==========================
# Récupère les boissons d'un joueur
def get_player_drinks_by_player_name(player_name):

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
# ========================== create_recipe ==========================
# Créer un/une ingrédient/recette
def create_recipe(recipe):

  db.execute("""
    INSERT INTO recipe
    VALUES('"""+recipe["recipe_name"]+"""',"""+recipe["recipe_price"]+""","""+recipe["recipe_alcohol"]+""","""+recipe["recipe_cold"]+""");
    """)

# ========================== get_day_number ==========================
# Renvoie le nombre du jour courrant
def get_current_day_number():

  db_day_response=db.select("""
    SELECT time_hour
    FROM time;
    """)

  return (int)(((int)(db_day_response[0]["time_hour"]))/24)

# ========================== day_exist_by_day_number ==========================
# Renvoie true si le jour existe, false sinon
def day_exist_by_day_number(day_number):

  row = db.select("\
    SELECT * FROM DAY\
    WHERE DAY_NUMBER = "+str(day_number)+";\
  ")

  if len(row) == 0 :

    return False

  else :

    return True

# ========================== get_available_ingredients ==========================
# Renvoie la liste des ingredients disponnible
# Wrong !
def get_available_ingredients(playerName):
  return get_ingredients()

# ========================== get_ingredients ==========================
# Renvoie la liste des ingredients
def get_ingredients():

  db_compose = db.select("""
    SELECT DISTINCT compose_ingredient_recipe_name
    FROM compose;""")

  db_recipe = db.select("""
    SELECT *
    FROM RECIPE;""")

  response = []

  for recipe in db_recipe :
    for ingredient in db_compose :
      if recipe["recipe_name"] == ingredient["compose_ingredient_recipe_name"] :
         response.append(recipe["recipe_name"])

  return response

# ========================== player_have_enough_budget_by_player_name ==========================
# Renvoie true si le joueur a assez d'argent, false sinon
def player_have_enough_budget_by_player_name(player_name,cost):
  db_player_response = db.select("""
    SELECT player_budget
    FROM player
    WHERE player_name = '"""+str(player_name)+"""';
  """)

  if len(db_player_response) == 1 :

    budget = float(db_player_response[0]["player_budget"])

    return budget >= float(cost)

# ========================== deduct_player_budget_by_player_name ==========================
# Déduit le budget du joueur en fonction du montant
def deduct_player_budget_by_player_name(player_name,amount):

  print("-- log deduct_player_budget_by_player_name -- : "+str(player_name))

  db_player_response = db.select("""
    SELECT player_budget
    FROM player
    WHERE player_name = '"""+str(player_name)+"""';
  """)

  print("-- log deduct_player_budget_by_player_name -- : "+str(db_player_response))

  if len(db_player_response) == 1 :

    budget = float(db_player_response[0]["player_budget"])

    new_budget = budget - float(amount)

    print("--log deduct_player_budget_by_player_name -- : "+str(new_budget))

    db.execute("""
      UPDATE player
      SET player_budget = """+str(new_budget)+"""
      WHERE player_name = '"""+str(player_name)+"""';
    """)

# ========================== recipe_quantity_produce_by_day_recipe_and_player ==========================
# renvoie le nombre de production par recette, jour et nom de joueur
def recipe_quantity_produce_by_day_recipe_and_player(current_day,item,sale_player_name) :

  db_sale_response = db.select("""
      SELECT sale_produce
      FROM sale
      WHERE sale_day_number = """+str(current_day)+"""
      AND sale_recipe_name = '"""+item+"""'
      AND sale_player_name = '"""+sale_player_name+"""';
    """)

  if len(db_sale_response) == 1 :

    return db_sale_response[0]["sale_produce"]

  else :

    return None

# ========================== calculate_all_sales ==========================
# calcul tout les coûts et déduit les montant sur le compte des joueurs
def calculate_all_sales() :

  current_day = get_current_day_number()

  db_sale_response = db.select("""
      SELECT *
      FROM sale
      WHERE sale_day_number = """+str(current_day)+""";
    """)

  print("-- log -- current_day : "+str(current_day))
  print("-- log -- db_sale_response : "+str(db_sale_response))

  for sale in db_sale_response :

    # Calcul le coût de production
    recipe_produce_price = float(get_recipe_produce_price_by_name(str(sale["sale_recipe_name"])))
    recipe_quantity_produce = float(recipe_quantity_produce_by_day_recipe_and_player(current_day,str(sale["sale_recipe_name"]),str(sale["sale_player_name"])))
    production_cost = recipe_quantity_produce * recipe_produce_price
    print("-- log -- recipe_produce_price"+str(recipe_produce_price))
    print("-- log -- recipe_quantity_produce"+str(recipe_quantity_produce))
    print("-- log -- production_cost"+str(production_cost))
    deduct_player_budget_by_player_name(str(sale["sale_player_name"]),production_cost)