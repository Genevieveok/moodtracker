from moodtracker import mood_app

#mood_app is created under moodtracker/_init.py_
app = mood_app()

#run app
# app.run(debug=True)
app.run(debug=True, host= '0.0.0.0',port='8080')