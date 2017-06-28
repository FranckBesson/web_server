# coding=utf-8

from db import Db
import json

db = Db()

def ingredients_get_request():
	# récupération des valeurs
	compose = get_compose()
	receipe = get_receipe()

	#création de l'ingrédient _ing
	_ing = {
	"compose" = compose
	"receipe" = receipe
	}

	#Création de l'objet à renvoyer
	response = {
	"ingredients" : _ing
	}

	for recipe in db_recipe_response :
		ingredientList.append(recipe)

	return json.dumps(ingredientList), 200, { "Content-Type": "application/json" }

def get_compose () :
	db_compose = db.select("""
		SELECT DISTINCT compose_ingredients_receipe_name
		FROM compose;""")

	db_receipe = db.select("""
		SELECT*
		FROM RECIPE;""")
