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

  	# Calcule le coût de production
  	recipe_produce_price = float(get_recipe_produce_price_by_name(item))
  	recipe_quantity_produce = float(recipe_quantity_produce_by_day_recipe_and_player(current_day,item,sale_player_name))
  	production_cost = recipe_quantity_produce * recipe_produce_price
  	deduct_player_budget_by_player_name(sale_player_name,production_cost)

  	db.execute("""
    	UPDATE SALE
    	SET sale_number = """+quantity+"""
    	WHERE sale_day_number = """+str(current_day)+"""
    	AND sale_recipe_name = '"""+item+"""'
    	AND sale_player_name = '"""+sale_player_name+"""';
  	""")

  return json.dumps(""), 200, { "Content-Type": "application/json" }