import os;

'''
        Title: GenerateInit.py
        ------------------------------------------------------------------
        Description: Auto generate our routing code from our page resources such 
        that we never have to edit the routing manually.
    
        Approach: Our file structure will contain a folder called pages. 
        Go through it and define routes+extra templates/resources associated with the page
'''

#Config options
config = {};
config["devActive"] = True;

toBeWritten = {};
toBeWritten["imports"]="import os\nimport pymongo\n";

toBeWritten["initMeat"]="\t@app.route(\"/\", methods=[\"GET\"])\n";
toBeWritten["initMeat"]+="\tdef homeRoute():\n\t\treturn redirect(\"/home\",302);\n"

toBeWritten["afterImports"]="from flask import Flask, render_template, redirect\nfrom flask_pymongo import PyMongo\n\ndef create_app(test_config=None):\n";
toBeWritten["afterImports"]+="\t# create and configure the app\n\tapp = Flask(__name__, instance_relative_config=True);\n";
toBeWritten["afterImports"]+="\tapp.config['MONGO_DBNAME'] = 'beat_warrior';\n\tapp.config[\"MONGO_URI\"] = \"mongodb://localhost:27017/beat_warrior\"\n\n";
toBeWritten["afterImports"]+="\tif test_config is None:\n\t\tapp.config.from_pyfile('config.py', silent=True);\n";
toBeWritten["afterImports"]+="\telse:\n\t\tapp.config.from_mapping(test_config);\n";
toBeWritten["afterImports"]+="\ttry:\n\t\t\tos.makedirs(app.instance_path);\n\texcept OSError:\n\t\tpass;\n\n";
toBeWritten["afterImports"]+="\tmongoDB = PyMongo(app);\n\tbeatCollection = mongoDB.db.test.find();\n\n";

#create our navbar
toBeWritten["navbar"]="""
<nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <a class="navbar-brand" href="/home">Home</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#primaryNavbar">
    <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="primaryNavbar">
""";

#read current file structure for pages
def findPages(_dir, _bufferDictionary):
    #store pages to construct so I only have to iterate once
    for filename in os.listdir(_dir):
        #Do I have sub directories that arent components?
        if os.path.isdir(_dir+'/'+filename):
            #gen navbar for this page
            temp = "";
            for i in range(_dir.count('/')):
                temp += "\t";
                
            #Am I component folders for the page?
            if(filename.lower() != "css" and filename.lower() != "js"):
                 #I am not, I am sub page hi
                _bufferDictionary["navbar"] += temp+"<li class=\"nav-item\">\n";
                _bufferDictionary["navbar"] += temp+"\t<a class=\"nav-link\" href=\""+filename+"\">"+filename+"</a>\n";

                _bufferDictionary["navbar"] += temp+"<ul class=\"navbar-nav\">\n";
                findPages(_dir+'/'+filename, _bufferDictionary);
                _bufferDictionary["navbar"] += temp+"</ul>\n";
                
            #close navbar for this page
            _bufferDictionary["navbar"] += temp+"</li>\n";
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
                file = open(_dir+'/'+filename, 'r');
                
                spl = file.readlines();

                file.close();
                
                constructPage(spl[0].replace('\n',""), _dir, spl[1].replace('\n',""), spl[2].replace('\n',""), _bufferDictionary, spl[3].replace('\n',""));
                
#helper function: construct a page
#------------------------------------------
#return: string | to append to tobe generated file
def constructPage(_name, _dir, _argumentHeaders, _vals, _bufferDict, _urlmethods=["GET"]):
    #import custom code if present to be called when routed
    foundPythonCode = False;
    if os.path.exists(_dir+'/'+_name+".py"):
        foundPythonCode = True;
        tdir = _dir[_dir.find("Website"):len(_dir)].replace("/",".");
        _bufferDict["imports"] += "import " + tdir+'.'+_name+"\n";

    _dir = _dir[54:len(_dir)];
    
    if _argumentHeaders != "":
        _argumentHeaders = "/"+_argumentHeaders;
        
    _bufferDict["initMeat"] += "\t@app.route(\"/"+_dir+_argumentHeaders+"\", methods="+_urlmethods+")\n";
    _bufferDict["initMeat"] += "\tdef " + _name +  _vals +"("+_argumentHeaders.replace("{","").replace("}","").replace("/","")+"):\n";
        
    if foundPythonCode:
        # preserved code
        _bufferDict["initMeat"] += "\t\ttry:\n";
        _bufferDict["initMeat"] += "\t\t\t"+_name+".preRender();\n";
        _bufferDict["initMeat"] += "\t\texcept Exception as error:\n";
        if config["devActive"]:
            toBeWritten["initMeat"] += "\t\t\tprint(error);\n";
        #_bufferDict["initMeat"] += "\t\telse:\n";
        
        _bufferDict["initMeat"] += "\t\ttemp =  render_template(\""+_dir+'/'+_name+".html\");\n";
        
        #postproccessed code
        _bufferDict["initMeat"] += "\t\ttry:\n";
        _bufferDict["initMeat"] += "\t\t\t"+_name+".postRender();\n";
        _bufferDict["initMeat"] += "\t\texcept Exception as error:\n";
        if config["devActive"]:
            _bufferDict["initMeat"] += "\t\t\tprint(error);\n";
        #_bufferDict["initMeat"] += "\t\telse:\n";
        
        _bufferDict["initMeat"] += "\t\treturn temp;\n";
    else:
        _bufferDict["initMeat"] += "\t\treturn render_template(\""+_dir+'/'+_name+".html\");\n";


#find all pages and process them
findPages("C:/Users/hmila/Desktop/Beat Warrior/Website/templates", toBeWritten);

#combine everything
    #routing file
toBeWritten["routing"] = toBeWritten["imports"] + toBeWritten["afterImports"] + toBeWritten["initMeat"] + "\n\treturn app";
    
    #navbar
toBeWritten['navbar'] += """
        </ul>
    </div>
</nav>
"""

#create actual files
file = open("testNavbar.html", "w");
file.write(toBeWritten["navbar"]);
file.close();

file = open("__init__.py", "w");
file.write(toBeWritten["routing"]);
file.close();
