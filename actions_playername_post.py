# coding=utf-8

from api import *
from db import Db
import json

db = Db()


def actions_playername_post_request(elements, playerName):

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
                    VALUES('"""+str(new_recipe["recipe_name"])+"""','"""+str(ingredient["name"])+"""');
                """)
                
        elif player_action["kind"] == "ad" :
    
            latitude = str(player_action["location"]["latitude"])
            longitude = str(player_action["location"]["longitude"])
            radius = str(player_action["radius"])
    
            db.execute("""
                INSERT INTO item(item_kind,item_influence,item_owner,item_x_coordinate,item_y_coordinate)
                VALUES('AD', """+radius+""",'"""+player_name+"""',"""+latitude+""","""+longitude+""");
                """)
    
        elif player_action["kind"] == "drinks" :
    
            sale_day_number = str(get_current_day_number()+1)
            sale_recipe_name = ""
            sale_produce = str(0)
            sale_player_name = playerName
            sale_number = str(0)
            sale_recipe_price = str(0)

            # Technique certainement gitanne et précaire mais d'apoint
            for key in player_action["prepare"]:

                sale_recipe_name = key
                sale_produce = str(player_action["prepare"][key])
                sale_recipe_price = str(player_action["price"][sale_recipe_name])
            
            db_sale_select = db.select("""
                SELECT *
                FROM SALE
                WHERE sale_day_number = """+sale_day_number+"""
                AND sale_recipe_name = '"""+sale_recipe_name+"""'
                AND sale_player_name = '"""+sale_player_name+"""';
                """)

            if len(db_sale_select) == 0 :

                db.execute("""
                    INSERT INTO SALE
                    VALUES("""+sale_day_number+""",'"""+sale_recipe_name+"""','"""+sale_player_name+"""',"""+sale_number+""","""+sale_produce+""","""+sale_recipe_price+""");
                """)

            else :

                db.execute("""
                    UPDATE SALE
                    SET sale_number = """+sale_number+""", sale_produce = """+sale_produce+""", sale_recipe_price = """+sale_recipe_price"""
                    WHERE sale_day_number = """+sale_day_number+"""
                    AND sale_recipe_name = """+sale_recipe_name+"""
                    AND sale_player_name = """+sale_player_name+""";
                """)


    return json.dumps(""), 200, { "Content-Type": "application/json" }