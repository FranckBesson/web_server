# coding=utf-8

# from db import Db
# import json
# 
# db = Db()
# 
# def ingredients_get_request():
# 	i =0
# 
# 	# Faire la requêtes pour récupérer les recette dont le nom apparait comme compose_ingredient_recipe_name dans compose
# 	db_recipe_response = db.select("""
#         SELECT compose_ingredient_recipe_name
#         FROM compose
# 		WHERE recipe_name<>compose_recipe_name
#         ORDER BY recipe_name;
#       """)
# 
# 	for recipe in db_recipe_response :
# 		ingredientList.append(recipe)
# 
# 	return json.dumps(ingredientList), 200, { "Content-Type": "application/json" }
