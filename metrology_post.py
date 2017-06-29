# coding=utf-8

from api import *
import json

def metrology_post_request(elements):

  forcast = elements["weather"]

  jour_actuel = (int)((int)(elements["timestamp"])/24)

  print(str("Day : "+jour_actuel))

  for weather in forcast :

    # Jour courrant
    if weather["dfn"] == "0" :
  
      set_day_weather_where_day_number(jour_actuel,weather["weather"])
  
    # Jour suivant
    elif weather["dfn"] == "1" :
  
      set_day_weather_where_day_number(jour_actuel+1,weather["weather"])
         
    insert_new_timestamp(elements["timestamp"])

  return json.dumps(""), 200, { "Content-Type": "application/json" }