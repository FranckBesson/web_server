# coding=utf-8

from db import Db
import json

def sales_post_request(elements):

  print(str(elements))

  sale_player_name = elements["sales"]["player"]
  item = elements["sales"]["item"]
  quantity = elements["sales"]["quantity"]

  db.execute("""
    UPDATE SALE
    SET sale_number = """+str(quantity)+"""
    WHERE sale_day_number = """+get_current_day_number()+"""
    AND sale_recipe_name = '"""+str(item)+"""'
    AND sale_player_name = '"""+sale_player_name+"""';
  """)

  return json.dumps(""), 200, { "Content-Type": "application/json" }