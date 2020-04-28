# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify

import json

app = Flask(__name__)


#### API ####
@app.route('/api/clients/')
def clients():
    with open('./data/clients.json') as json_file:
        data = json.load(json_file)
    return jsonify({
      'status': 'ok', 
      'data': data
    })
   



#### Main ####

if __name__ == "__main__":
    app.run(debug=True)