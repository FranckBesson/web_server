# coding=utf-8

from db import Db
import json

def reset_get_request():
	return json.dumps(""), 200, { "Content-Type": "application/json" }