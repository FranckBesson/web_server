# coding=utf-8

from api import *
from db import Db
import json

db = Db()


def actions_playername_post_request(elements, playerName):
    print(str(elements))
    player_actions = elements["actions"]
    player_name = str(playerName)

    for player_action in player_actions :
    
        if player_action["kind"] == "recipe" :
    
            recipe = player_action["recipe"]
    
            recipe_alcohol = "false"
    
            recipe_cold = "false"
    
            for ingredient in recipe["ingredients"] :
    
                if (ingredient["hasAlcohol"]).lower() == "true" :
    
                    recipe_alcohol = "true"
    
                if (ingredient["recipe_cold"]).lower() == "true" :
    
                    recipe_cold = "true"
    
            # How to know the recipe price ?
    
            # Création de la recette
            new_recipe = {
            "recipe_name" : recipe["name"],
            "recipe_price" : 1,
            "recipe_alcohol" : recipe_alcohol,
            "recipe_cold" : recipe_cold
            }
    
            create_recipe(new_recipe)
    
            for ingredient in recipe["ingredients"] :
    
                db.execute("""
                    INSERT INTO compose
                    VALUES('"""+new_recipe["recipe_name"]+"""','"""+ingredient["name"]+"""');
                """)
                
        elif player_action["kind"] == "ad" :
    
            latitude = player_action["location"]["latitude"]
            longitude = player_action["location"]["longitude"]
            radius = player_action["radius"]
    
            db.execute("""INSERT INTO item VALUES('AD', """+radius+""",'"""+player_name+"""',"""+latitude+""","""+longitude+""");""")
    
        elif player_action["kind"] == "drinks" :
    
            sale_day_number = str(get_current_day_number()+1)
            sale_recipe_name = ""
            sale_produce = 0
            sale_player_name = playerName
            sale_number = 0
            sale_recipe_price = 0

            # Technique certainement gitanne et précaire mais d'apoint
            for key in player_action["prepare"]:

                sale_recipe_name = key
                sale_produce = player_action["prepare"][key]
                player_action["price"][sale_recipe_name]
            
            sale_recipe_price =
    
            db.execute("""
                INSERT INTO SALE
                VALUES("""+sale_day_number+""",'"""+sale_recipe_name+"""','"""+sale_player_name+"""',"""+player_action[""]+""","""+sale_produce+""","""+sale_recipe_price+""");
            """)
    
    return json.dumps(""), 200, { "Content-Type": "application/json" }