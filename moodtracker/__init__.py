"""Initialize flask applictation"""
# from flask import Flask

# #app = Flask(__name__)
# app = Flask(__name__, instance_relative_config=True) #instance/config overrides regular config.py

# #we can access the configuration variables via app.config["VAR_NAME"].
# #app.config.from_object('config') #for config variables in config.py
# app.config.from_pyfile('config.py')  #instance/config overrides regular config.py


# from moodtracker import views
# from moodtracker import models

# app.run()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#db_name = 'mood.db' #database


def mood_app():
    #create main application
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    db.init_app(app)

    with app.app_context():
        from . import views  #import views(routes) to be run
        db.create_all()  #create tables for data models

        return app

