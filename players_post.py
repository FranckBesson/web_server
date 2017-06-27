# coding=utf-8
from api import *
import json

# ========================== players_post_request ==========================
# Requête pour log un utilisateur
def players_post_request(elements):

  name = str(elements["name"])

  if player_exist(name) == False :

  	while i <= 1500 :

    	create_player_by_name(str(name+str(i)))

    	i = i +1
    
    print("ouf")

  response = {
    "name" : name,
    "location" : get_player_location_by_player_name(name),
    "info" : get_player_info_by_player_name(name)
  }

  return json.dumps(response), 200, { "Content-Type": "application/json" }

