# coding=utf-8

from db import Db
import json

db = Db()

def ingredients_get_request():

	# récupération des valeurs
	ingredients = get_ingredients()

	return json.dumps(ingredients), 200, { "Content-Type": "application/json" }

def get_ingredients ():
	db_compose = db.select("""
		SELECT DISTINCT compose_ingredients_recipe_name
		FROM compose;""")

	db_recipe = db.select("""
		SELECT *
		FROM RECIPE;""")

	tab = []

	for recipe in db_recipe
		for ingredient in db_compose
			if recipe["recipe_name"] == compose["compose_ingredients_recipe_name"]
				 tab.append(recipe["recipe_name"])
	return tab