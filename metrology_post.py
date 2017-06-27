# coding=utf-8

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
  
      row = db.select("\
        SELECT * FROM DAY\
        WHERE DAY_NUMBER = "+str(jour_actuel)+";\
      ")
  
      if len(row) == 0 :
        
        print("-- log-- insert with dfn at 0 : "+str(row))

        db.execute("""
          INSERT INTO DAY
          VALUES("""+str(jour_actuel)+""",'"""+str(weather["weather"])+"""');
        """)
  
      else :

        print("-- log-- update with dfn at 0")

        db.execute("""
          UPDATE DAY SET DAY_WEATHER = '"""+str(weather["weather"])+"""'
          WHERE DAY_NUMBER = '+str(jour_actuel)+';
        """)
  
    # Jour suivant
    elif weather["dfn"] == "1" :
    
      row = db.select("\
        SELECT * FROM DAY\
        WHERE DAY_NUMBER = "+str(jour_actuel+1)+";\
      ")
  
      if len(row) == 0 :
  
        print("-- log-- insert with dfn at 1")

        db.execute("""
          INSERT INTO DAY
          VALUES("""+str(jour_actuel+1)+""",'"""+str(weather["weather"])+"""');
        """)
  
      else :
  
        print("-- log-- update with dfn at 1")

        db.execute("""
          UPDATE DAY SET DAY_WEATHER = '"""+str(weather["weather"])+"""'
          WHERE DAY_NUMBER = """+str(jour_actuel+1)+""";
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