import os
import pymongo
import Website.templates.home.home
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True);
	app.config['MONGO_DBNAME'] = 'beat_warrior';
	app.config["MONGO_URI"] = "mongodb://localhost:27017/beat_warrior"

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True);
	else:
		app.config.from_mapping(test_config);
	try:
			os.makedirs(app.instance_path);
	except OSError:
		pass;

	mongoDB = PyMongo(app);
	beatCollection = mongoDB.db.test.find();

	@app.route("/", methods=["GET"])
	def homeRoute():
		return redirect("/home",302);
	@app.route("/home", methods=["GET", "POST"])
	def home():
		try:
			home.preRender();
		except Exception as error:
			print(error);
		temp =  render_template("home/home.html");
		try:
			home.postRender();
		except Exception as error:
			print(error);
		return temp;

	return app