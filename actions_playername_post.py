# coding=utf-8

from api import *
from db import Db
import json

db = Db()

def actions_playername_post_request(elements, playerName):

    player_actions = elements["actions"]
    player_name = str(playerName)

    cost = 0.0

    for player_action in player_actions :
    
        if player_action["kind"] == "ad" :

            cost += float(player_action["radius"]) * 10.0

        elif player_action["kind"] == "drinks" :

            # Technique certainement gitanne et précaire mais d'apoint
            for key in player_action["prepare"]:

                sale_recipe_name = key
                sale_produce = player_action["prepare"][key]
    
                cost += float(sale_produce) * float(get_recipe_produce_price_by_name(str(sale_recipe_name)))

    if player_have_enough_budget_by_player_name(player_name, cost) :

        for player_action in player_actions :
        
            if player_action["kind"] == "recipe" :
        
                player_action_recipe(player_action,player_name)
                    
            elif player_action["kind"] == "ad" :
        
                player_action_ad(player_action,player_name)
    
            elif player_action["kind"] == "drinks" :
        
                player_action_drinks(player_action,player_name)

        response = {
            "sufficientFunds" : True,
            "totalCost" : cost
        }

        return json.dumps(response), 200, { "Content-Type": "application/json" }

    else :

        response = {
            "sufficientFunds" : False,
            "totalCost" : cost
        }

        return json.dumps(response), 200, { "Content-Type": "application/json" }