# coding=utf-8

from db import Db
import json

def map_playername_get_request():
	return json.dumps(""), 200, { "Content-Type": "application/json" }