# coding=utf-8

from db import Db
import json

def ingredients_get_request():
	i =0

	db_recipe_response = db.select("""
        SELECT *
        FROM RECIPE
		WHERE recipe_name<>compose_recipe_name
        ORDER BY recipe_name;
      """)

	ingredients = db_recipe_response[0]

	ingredientInfo = {
	  "name" : db_recipe_response[0]["recipe_name"],
	  "price" : get_recipe_produce_price_by_name(db_recipe_response[0]["recipe_name"]),
	  "hasAlcohol" : db_recipe_response[0]["recipe_alcohol"],
	  "isCold" : db_recipe_response[0]["recipe_cold"]
	}

	while ():
		ingredientList[i] = db_recipe_response[i]["recipe_name"]
		i++

	return json.dumps(ingredientList), 200, { "Content-Type": "application/json" }
