from moodtracker import app
from flask import Flask
from flask import request,render_template,redirect,url_for
 

#app = Flask(__name__)
 

@app.route('/')
def hello_world():
    return redirect(url_for('log_in'))

@app.route('/create')
def create_account():
    error = None
    return render_template('create.html', error=error)
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return 'Hello World'
 
# Route for handling the login page logic
@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
 
    app.run()
