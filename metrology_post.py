# coding=utf-8

from db import Db
import json

def metrology_post_request(elements):

  print("-- log -- elements : " + str(elements))
  print("-- log -- timestamp : " + str(elements["timestamp"]))
  weather = str(elements["weather"]["weather"])
  print("-- log -- weather : " + weather)

  db = Db()

  jour_actuel = (int)((int)(elements["timestamp"])/24)
  print(str(jour_actuel))

  
  # Jour courrant
  if elements["weather"]["dfn"] == "0" :

    print("current day")

    row = db.select("\
      SELECT * FROM DAY\
      WHERE DAY_NUMBER = "+str(jour_actuel)+";\
    ")

    print(str(row))

    if len(row) == 0 :

      db.execute("\
        INSERT INTO DAY\
        VALUES("+str(jour_actuel)+",\'"+str(weather)+"\');\
      ")

    else :

      db.execute("\
        UPDATE DAY SET DAY_WEATHER = \'"+str(weather)+"\'\
        WHERE DAY_NUMBER = "+str(jour_actuel)+";\
      ")

  # Jour suivant
  elif elements["weather"]["dfn"] == "1" :

    print("day after")

    row = db.select("\
      SELECT * FROM DAY\
      WHERE DAY_NUMBER = "+str(jour_actuel+1)+";\
    ")

    print(str(row))

    if len(row) == 0 :

      db.execute("\
        INSERT INTO DAY\
        VALUES("+str(jour_actuel+1)+",\'"+str(weather)+"\');\
      ")

    else :

      db.execute("\
        UPDATE DAY SET DAY_WEATHER = \'"+str(weather)+"\'\
        WHERE DAY_NUMBER = "+str(jour_actuel+1)+";\
      ")

  #Sauvegarde du timestamp
  db.execute("\
        DELETE FROM TIME;\
      ")

  db.execute("\
        INSERT INTO TIME\
        VALUES("+str(elements["timestamp"])+");\
      ")

  db.close()

  return json.dumps(""), 200, { "Content-Type": "application/json" }