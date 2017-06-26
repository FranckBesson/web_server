# coding=utf-8

from api import *
import json

def map_get_request():

  # Récupération des valeurs
  region = get_region()
  ranking = get_ranking() 
  itemsByPlayer = get_item_by_player()
  playerinfo = get_player_info()
  drinksByPlayer = get_drinks_by_player()

  # Création de la map _map
  _map = {
    "region" : region,
    "ranking" : ranking,
    "itemsByPlayer" : itemsByPlayer,
    "playerInfo" : playerinfo,
    "drinksByPlayer" : drinksByPlayer
  }

  #Création de l'objet à renvoyer
  response = {
    "map" : _map
  }

  return json.dumps(response), 200, { "Content-Type": "application/json" }