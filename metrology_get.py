# coding=utf-8

from api import *
import json

def metrology_get_request():
  
  weathers = []

  # On récupère le jour actuel
  weather_today = get_weather_today()

  if weather_today != False :

    weathers.append(weather_today)

  # On récupère le jour de demain
  weather_tomorrow = get_weather_tomorrow()

  if weather_tomorrow != False :

    weathers.append(weather_tomorrow)

  #Création de l'objet à renvoyer
  response = {
    "timestamp" : get_timestamp(),
    "weather" : weathers
  }
  
  return json.dumps(response), 200, { "Content-Type": "application/json" }