from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route("/")
def helloWorld():
  return "Works !"
 
if __name__ == "__main__" :
   app.run()
