from flask import Flask

#app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True) #instance/config overrides regular config.py

#we can access the configuration variables via app.config["VAR_NAME"].
#app.config.from_object('config') #for config variables in config.py
app.config.from_pyfile('config.py')  #instance/config overrides regular config.py


from moodtracker import views
from moodtracker import models

app.run()
