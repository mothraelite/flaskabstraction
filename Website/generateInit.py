import os;

'''
        Title: GenerateInit.py
        ------------------------------------------------------------------
        Description: Auto generate our routing code from our page resources such 
        that we never have to edit the routing manually.
    
        Approach: Our file structure will contain a folder called pages. 
        Go through it and define routes+extra templates/resources associated with the page
'''

#Create the base page in text
toGenerate = """
import os
import pymongo
from flask import Flask
from flask_pymongo import PyMongo

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True);
    app.config['MONGO_DBNAME'] = 'beat_warrior';
    app.config["MONGO_URI"] = "mongodb://localhost:27017/beat_warrior";
	
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True);
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config);

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path);
    except OSError:
        pass;

	#mango connection
    mongoDB = PyMongo(app);
    beatCollection = mongoDB.db.test.find();

        
"""

#read current file structure for pages
def findPages(_dir):
    for filename in os.listdir(_dir):
        #Do I have sub directories that arent components?
        if os.path.isfile(filename):
            #Am I component folders for the page?
            if(filename.lower() != "css" && filename.lower() != "js"):
                #I am not, I am sub page hi
                findPages(_dir/filename);
        else:
            #Find config file to start processing
            if(filename.lower() == "config.txt"):
                #      read info
                #----------------------
                #Rule: Delimited by new lines
                #1) String | Page url name 
                #2) String | argument url header //has formatting done already
                #2) String | Arguments list
                #3) String | url methods
                file = open(filename, 'r');
                
                name = file.readline();
                argumentHeader = file.readline();
                args = file.readline();
                urlmethods = file.readline();
                
                file.close();
                
                constructPage(name, _dir, argumentHeader, args, urlmethods);
            
    return toGenerate;
                
#helper function: construct a page
#------------------------------------------
#return: string | to append to tobe generated file
def constructPage(_name, _dir, _argumentHeaders, _args, _urlmethods=["GET"]):
        toGenerate += "\t@app.route(\"/"+_dir+'/'+_name+_argumentHeaders+"\", methods="+_urlmethods+")\n";
        toGenerate += "\tdef " + _name +  args +":\n";
        toGenerate += "\t\t";
    
    