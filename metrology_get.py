# coding=utf-8

# R1 Commande temps (GET)
# Par le client web et le simulateur java
@app.route("/metrology", methods=['GET'])
def metrology_get():
  
  db = Db()

  # Requête pour connaitre le jour actuel
  db_time_response = db.select("\
      SELECT * FROM time;\
    ")
  timestamp = (int)(db_time_response[0]["time_hour"])
  # Log
  print("-- log -- current timestamp : "+str(timestamp))
  current_day_number = (int)(timestamp/24)
  print("-- log -- current day number : "+str(current_day_number))

  # Ce tableau contiendra tout les objet "weather"
  weathers = []

  # On récupère le jour actuel
  db_current_weather_response = db.select("\
      SELECT day_weather FROM day\
      WHERE day_number = "+str(current_day_number)+";\
    ")

  # On test pour voir si le jour actuel est en base de donnée
  if len(db_current_weather_response) == 1 :

    print("-- log -- current day weather : "+str(db_current_weather_response[0]["day_weather"]))

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

    print("-- log -- tomorrow day weather : "+str(db_tomorrow_weather_response[0]["day_weather"]))

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

  # Log
  print("-- log -- response : "+str(response))

  db.close()
  
  return json_response(response)