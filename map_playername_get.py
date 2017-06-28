# coding=utf-8

from db import Db
import json

def map_playername_get_request(playerName):

	_map = {
		"region" : get_region(),
		"ranking" : get_ranking() ,
		"itemsByPlayer" : get_item_by_player()
	}

	response = {
		"availableIngredients" : "Si Fabien y arrive ...",
		"map" : _map,
		"playerInfo" : get_player_info_by_player_name(playerName)
	}

	return json.dumps(response), 200, { "Content-Type": "application/json" }