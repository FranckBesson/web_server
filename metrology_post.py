# coding=utf-8

from api import *
from db import Db
import json

def metrology_post_request(elements):

  forcast = elements["weather"]

  db = Db()

  jour_actuel = (int)((int)(elements["timestamp"])/24)
  print(str(jour_actuel))

  for weather in forcast :

    print("-- log--"+str(weather))
    # Jour courrant
    if weather["dfn"] == "0" :
  
      if day_exist_by_day_number(jour_actuel) :

        print("-- log-- update with dfn at 0")
        
        db.execute("""
          UPDATE DAY SET DAY_WEATHER = '"""+str(weather["weather"]).upper()+"""'
          WHERE DAY_NUMBER = """+str(jour_actuel)+""";
        """)
  
      else :
        
        print("-- log-- insert with dfn at 0 : ")

        db.execute("""
          INSERT INTO DAY
          VALUES("""+str(jour_actuel)+""",'"""+str(weather["weather"]).upper()+"""');
        """)
  
    # Jour suivant
    elif weather["dfn"] == "1" :
  
      if day_exist_by_day_number(jour_actuel+1) :
  
        print("-- log-- update with dfn at 1")

        db.execute("""
          UPDATE DAY SET DAY_WEATHER = '"""+str(weather["weather"]).upper()+"""'
          WHERE DAY_NUMBER = """+str(jour_actuel+1)+""";
        """)
  
      else :
    
        print("-- log-- insert with dfn at 1")

        db.execute("""
          INSERT INTO DAY
          VALUES("""+str(jour_actuel+1)+""",'"""+str(weather["weather"]).upper()+"""');
        """)
         
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