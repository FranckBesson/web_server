# coding=utf-8

from db import Db
import json

db = Db()

def ingredients_get_request():
	return json.dumps(get_ingredients()), 200, { "Content-Type": "application/json" }