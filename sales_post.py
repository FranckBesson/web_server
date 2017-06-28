# coding=utf-8

from api import *
from db import Db
import json

db = Db()

def sales_post_request(elements):

  sales = elements["sales"]

  for sale in sales :

  	sale_player_name = str(sale["player"])
  	item = str(sale["item"])
  	quantity = str(sale["quantity"])

  	db.execute("""
    	UPDATE SALE
    	SET sale_number = """+quantity+"""
    	WHERE sale_day_number = """+str(get_current_day_number())+"""
    	AND sale_recipe_name = '"""+item+"""'
    	AND sale_player_name = '"""+sale_player_name+"""';
  	""")

  return json.dumps(""), 200, { "Content-Type": "application/json" }