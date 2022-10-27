#from moodtracker import app
from flask import current_app as app
from flask import Flask
from flask import request,render_template,redirect,url_for, make_response, flash
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
from datetime import datetime as dt
 
from .models import db, User, CollectiveMood, Mood
#app = Flask(__name__)
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'log_in'

@app.route('/')
def welcome():
    return redirect(url_for('log_in'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/create_acc',methods=['GET', 'POST'])
def create_acc():
    error = None
    msg=None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        names = request.form['names']
        password = request.form['password']
        
        if User.query.filter_by(email=email).first():
            error = "User already exists. Please log into account"
            flash('User with email already exists',category='error')
            return render_template('create.html', error=error)

        if User.query.filter_by(username=username).first():
            error = "User already exists. Please try another username"
            flash('Username already exists',category='error')
            
            return render_template('create.html', error=error)

        if username and email and names and password:
            new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            names =names,
            password=password
            )
            db.session.add(new_user)  # Adds new User record to database
            db.session.commit()  # Commits all changes
            msg = username+" successfully created! Please log in"
            flash('Username successfully created!')
            return render_template('create.html', msg=msg)
        else:

            attributes =["username","password","email","names"]

            for val in attributes:

                if request.form[val]== None:
                    error = val+" missing"
                    flash('Please enter correct '+val,category='error')
                    break

    
    return render_template('create.html', error=error)
    return redirect(url_for('home'))

@app.route('/home')
@login_required
def home():
    error = None
    return render_template('options.html', error=error)
 

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not User.query.filter_by(username=username,password=password).first():
        #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            flash('Login not successful',category='error')
        else:
            user = User.query.filter_by(username=request.form['username']).first()
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/log_out')
def log_out():
    logout_user()
    return redirect(url_for('log_in'))


@app.route('/forgot_pass')
def forgot_pass():
    pass

@app.route('/del')
def delete_user():
    """ Personal function for deleting users from database"""
    user = "gen3"
    db.session.query(User).filter(User.username==user).delete()
    db.session.commit()
    return user + " deleted!"

@app.route('/del2')
def delete_cm():
    """ Personal function for deleting cm from database"""
    user = 4
    db.session.query(CollectiveMood).filter(CollectiveMood.userid==user).delete()
    db.session.commit()
    return str(user) + " deleted!"

@app.route('/view_mood')
@login_required
def view_mood():
    error = None
    userid = current_user.get_id()
    data = CollectiveMood.query.get(userid)
    dicts={}
    
    if data:
        datastring = data.allmood.split('|')
        datastring.pop()
        if datastring:
            for arr in datastring:
                newdatastring = arr.split(';')
                dicts[newdatastring[2]+newdatastring[1]] = newdatastring[0]

    else:
        error = "No mood data exists"
        flash('No mood exists',category='error')
    
    return render_template('viewmood.html', val=dicts,error = error)

    

@app.route('/enter_mood')
@login_required
def enter_mood():
    #print("Mood entered")
    userid = current_user.get_id()
    usermood = CollectiveMood.query.get(userid)
    mood = "red"
    day = dt.now().strftime("%d")
    month = dt.now().strftime("%b")


    if not usermood:
        # value = {"mood":mood,"day":day,"month":month}
        # value = "mood:'{}',day:{},month:'{}'".format(mood, day, month)
        # value = "{"+value+"}"
        value = mood+";"+day+";"+month+"|";
        moods= CollectiveMood(
            userid = userid,
            allmood = str(value),
        )
        db.session.add(moods)  
        db.session.commit()
        return redirect(url_for('view_mood'))



    if userid and mood and day and month:
        # value = "mood:{},day:{},month:{}".format(mood, day, month)
        # value = {"mood":mood,"day":day,"month":month}
        # value = ";{"+value+"}"
        value = mood+";"+day+";"+month+"|";
        usermood.allmood = usermood.allmood+value
        db.session.commit()  
    
    return redirect(url_for('view_mood'))

@app.route('/test', methods=['GET'])
def user_info():
    """create user test."""
    username = "admin"
    email = "admin"#request.args.get('email')
    names = "names name"
    password ="admin"
    if username and email:
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            names =names,
            password=password
        )
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
    return make_response(f"{new_user} successfully created!")

if __name__ == '__main__':
 
    app.run()
