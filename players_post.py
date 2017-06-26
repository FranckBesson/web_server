# coding=utf-8

from db import Db
import json

def players_post_request(elements):
  	print(str(elements))
	return json.dumps(""), 200, { "Content-Type": "application/json" }