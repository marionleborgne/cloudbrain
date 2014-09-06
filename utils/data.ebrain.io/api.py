__author__ = 'marion'

from flask import Flask
from flask.ext.pymongo import PyMongo
import json
import urlib

db_name = "cloudbrain"
app = Flask(db_name)
mongo = PyMongo(app)

@app.route('/')
def home_page():
    return "CloudbrainDB API"


@app.route('/label_sample/<label>')
def user_profile(label):
    testData = mongo.db.testData.find_one_or_404({'label': label})
    testData.pop('_id', None)
    return json.dumps(testData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)