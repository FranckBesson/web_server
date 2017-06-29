# coding=utf-8

from api import *
from db import Db
import json

db = Db()

def sales_post_request(elements):

  print(elements)

  sales = elements["sales"]

  for sale in sales :

	current_day = get_current_day_number()

	# On caste la valeur de quantity pour pas que le joueur ne vende plus de boisson
	cast_quantity_value_for_sale(str(sale["quantity"]),current_day,str(sale["item"]),str(sale["player"]))

	# Mise à jour de la table sale pour prendre en compte les ventes
	db.execute("""
		UPDATE SALE
		SET sale_number = """+str(sale["quantity"])+"""
		WHERE sale_day_number = """+str(current_day)+"""
		AND sale_recipe_name = '"""+str(sale["item"])+"""'
		AND sale_player_name = '"""+str(sale["player"])+"""';
	""")

  # Effectue une mise à jour du budget de tout les joueurs
  calculate_all_sales()

  return json.dumps(""), 200, { "Content-Type": "application/json" }	