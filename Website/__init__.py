import os
import pymongo
from flask import Flask
from flask_pymongo import PyMongo

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MONGO_DBNAME'] = 'beat_warrior'
    app.config["MONGO_URI"] = "mongodb://localhost:27017/beat_warrior"
	
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

	#mango test connection
    mongoDB = PyMongo(app);
    beatCollection = mongoDB.db.test.find();
    
    # Home page
    @app.route('/', methods=['GET', 'POST'])
    def home():
        return beatCollection[0]["title"];

    return app;