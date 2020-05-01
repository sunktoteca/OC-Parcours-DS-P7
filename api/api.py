# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify

import json

app = Flask(__name__)


#### API ####
@app.route('/api/clients/')
def clients():
    with open('./data/clients.json') as json_file:
        clients = json.load(json_file)
    with open('./data/histo.json') as json_file:
        histo = json.load(json_file)
    return jsonify({
      'status': 'ok', 
      'clients': clients,
      'histo': histo
    })
   



#### Main ####

if __name__ == "__main__":
    app.run(debug=True)