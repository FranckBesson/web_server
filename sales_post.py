# coding=utf-8

from api import *
from db import Db
import json

db = Db()

def sales_post_request(elements):

  print(elements)

  sales = elements["sales"]

  for sale in sales :

	sale_player_name = str(sale["player"])
	item = str(sale["item"])
	quantity = str(sale["quantity"])

	current_day = get_current_day_number()

	# Je caste la valeur de quantité pour pas le joueur vende plus de boissons qu'il n'en produise
	db_sale_select = db.select("""
		SELECT *
		FROM SALE
		WHERE sale_day_number = """+str(current_day+1)+"""
		AND sale_recipe_name = '"""+str(item)+"""'
		AND sale_player_name = '"""+str(sale_player_name)+"""';
	""")

	print("-- log -- sales_post_request : "+str(db_sale_select))

	if len(db_sale_select) == 1 :

		productions = float(db_sale_select[0]["sale_produce"])

		if quantity > productions :

			quantity = productions

	db.execute("""
		UPDATE SALE
		SET sale_number = """+str(quantity)+"""
		WHERE sale_day_number = """+str(current_day+1)+"""
		AND sale_recipe_name = '"""+str(item)+"""'
		AND sale_player_name = '"""+str(sale_player_name)+"""';
	""")

  calculate_all_sales()

  return json.dumps(""), 200, { "Content-Type": "application/json" }