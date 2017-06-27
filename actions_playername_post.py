# coding=utf-8

from api import *
from db import Db
import json

db = Db()


def actions_playername_post_request(elements, playerName):
    player_action = elements["actions"]
    player_name = str(playerName)

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

        db.execute("""
            INSERT INTO SALE
            VALUES("""+get_current_day_number()+""",'"""+player_action["prepare"][""]+"""','"""+str(playerName)+"""',"""+player_action[""]+""",);
         """)

    return json.dumps(""), 200, { "Content-Type": "application/json" }