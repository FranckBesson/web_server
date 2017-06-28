# coding=utf-8

from db import Db
import json

def metrology_get_request():

  db = Db()

  # Requête pour connaitre le jour actuel
  db_time_response = db.select("\
      SELECT * FROM time;\
    ")

  timestamp = 0

  if len(db_time_response) == 1 :

    timestamp = (int)(db_time_response[0]["time_hour"])

  else :

    return json.dumps("error in bd, no timestamp in the table"), 500, { "Content-Type": "application/json" }
  
  current_day_number = (int)(timestamp/24)

  # Ce tableau contiendra tout les objet "weather"
  weathers = []

  # On récupère le jour actuel
  db_current_weather_response = db.select("\
      SELECT day_weather FROM day\
      WHERE day_number = "+str(current_day_number)+";\
    ")

  # On test pour voir si le jour actuel est en base de donnée
  if len(db_current_weather_response) == 1 :

    # On crée une map weather_today
    weather_today = {
      "dfn" : 0,
      "weather" : str(db_current_weather_response[0]["day_weather"])
    }

    # On l'ajoute à la liste
    weathers.append(weather_today)

  # On récupère le jour de demain
  db_tomorrow_weather_response = db.select("\
      SELECT day_weather FROM day\
      WHERE day_number = "+str(current_day_number+1)+";\
    ")

  # On test pour voir si le jour de demain est en base de donnée
  if len(db_tomorrow_weather_response) == 1 :

    # On crée une map weather_tomorrow
    weather_tomorrow = {
      "dfn" : 1,
      "weather" : str(db_tomorrow_weather_response[0]["day_weather"])
    }

    # On l'ajoute à la liste
    weathers.append(weather_tomorrow)

  #Création de l'objet à renvoyer
  response = {
    "timestamp" : timestamp,
    "weather" : weathers
  }

  db.close()
  
  return json.dumps(response), 200, { "Content-Type": "application/json" }