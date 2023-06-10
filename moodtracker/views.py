#from moodtracker import app
from flask import current_app as app
import re
import jwt
import os
from threading import Thread
from time import time
from flask import Flask, jsonify
from flask import request,render_template,redirect,url_for, make_response, flash
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
from datetime import datetime as dt
from flask_mail import Mail, Message
mail = Mail(app)
 
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

        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

        if not EMAIL_REGEX.match(email):
            flash('Please add a valid email.',category='error')
            return render_template('create.html', error=error)
        
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
    
    return redirect(url_for('view_mood'))
 

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

def get_reset_token(user, expires=500):
    return jwt.encode({'reset_password': user, 'exp':   time() + expires}, key=app.config.get('SECRET_KEY','TEST'),algorithm='HS256')

@app.route('/verify_reset_token', methods=['GET', 'POST'])
def verify_reset_token():
    token = request.args.get('token')
    
    try:
        username = jwt.decode(token,key=app.config.get('SECRET_KEY','TEST'), algorithms=['HS256'])['reset_password']
        
    except Exception as e:
        print(e)
        return  "Reset expired or invalid. Please try resetting password again or contact support."
    
    return redirect(url_for('reset',email=username))


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    error = None
    email=request.args.get('email')


    if request.method == 'POST':
        if email:
            password = request.form['password']
            
            if not User.query.filter_by(email=email).first():

                flash('Reset not possible. User does not exist or reset request has expired.',category='error')
            else:
                #update db with new password
                usernow = User.query.filter_by(email=email).first()
                usernow.password = password
                db.session.commit()
                flash("Reset successful. Please log in.")
                return redirect(url_for('log_in'))
        else:
            flash('Reset not possible. User does not exist or reset request has expired.',category='error')


    return render_template('resetpassword.html')

def send_email(email):

    token = get_reset_token(email)

    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender = app.config.get('MAIL_USERNAME',None)
    msg.recipients = [email]
    usernow = User.query.filter_by(email=email).first()
    # msg.body = 'Email body'
    msg.html = render_template('message.html',
                                username=usernow.username, 
                                token=token)

    with app.app_context():
    # with app.test_request_context:
        mail.send(msg)
        
    return True

@app.route('/forgot_pass',methods=['GET', 'POST'])
def forgot_pass():

    error = None
    msg=None
    currapp = app
    
    if request.method == 'POST':      
        email = request.form['email']
        if User.query.filter_by(email=email).first():
            
            flash('User with email exists. Reset email has been sent.')
            # if Thread(target=send_email, args=(currapp,msg,email,)).start():
            if send_email(email):
                return render_template('resetemail.html', error=error)
            else:
                flash( "Reset cannot be completed. Please try again or contact us with more details on this issue.",category='error')
        else:
            flash('No user with this email exists',category='error')

    return render_template('resetemail.html', error=error)

@app.route('/del')
def delete_user():
    """ Personal function for deleting users from database"""
    user = "admins"
    db.session.query(User).filter(User.username==user).delete()
    db.session.commit()
    return user + " deleted!"

@app.route('/delmood')
def delete_cm():
    """ Personal function for deleting collective mood from database"""
    user = 3
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
    
    #for testing
    # f = open('dbsimulationtest.txt', 'r')
    # content = f.read()
    # data = content

    if data:
        # datastring = data.split('|') #for testing
        datastring = data.allmood.split('|')
        datastring.pop()
        if datastring:
            for arr in datastring:
                newdatastring = arr.split(';')
                dicts[newdatastring[2]+newdatastring[1]] = newdatastring[0]

    else:
        error = "No mood data exists yet"
        flash('No mood exists',category='error')
    
    return render_template('viewmood.html', val=dicts,error = error)

    

@app.route('/enter_mood',methods=['GET', 'POST'])
@login_required
def enter_mood():
    #print("Mood entered")
    day = dt.now().strftime("%d")
    month = dt.now().strftime("%b")
    year = dt.now().strftime("%Y")
    error = None
    today = f"{month} {day} {year}"

    if request.method == 'POST':
        print("heres")
        labelid = request.form['submit_button'] 
        userid = current_user.get_id()
        usermood = CollectiveMood.query.get(userid)
        mood = labelid
        msg=None
        # msg = "Thanks for entering your mood!"
        print(labelid)

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
            #return redirect(url_for('view_mood'))
            flash('Mood entered for today!')
            return render_template('entermood.html', msg =msg, today = today, error = error)



        if userid and mood and day and month:
            # value = "mood:{},day:{},month:{}".format(mood, day, month)
            # value = {"mood":mood,"day":day,"month":month}
            # value = ";{"+value+"}"
            value = mood+";"+day+";"+month+"|";
            usermood.allmood = usermood.allmood+value
            db.session.commit()  
            flash('Mood entered for today!')
        
        #return redirect(url_for('view_mood'))
        return render_template('entermood.html', msg =msg, today = today, error = error)
    return render_template('entermood.html', today = today, error = error)

@app.route('/test', methods=['GET'])
def user_info():
    """ Personal function for creating test user"""
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
