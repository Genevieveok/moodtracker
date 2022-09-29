from flask import Flask

app = Flask(__name__)


from moodtracker import views
from moodtracker import models

app.run(debug=True)
