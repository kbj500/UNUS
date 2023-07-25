from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from website.spotify_client import SpotifyClient


#client_id = "63b042243c2548b5b3ebb02756e84cb4"
#client_secret = "96bc8bc908894f9ab922ac0f0d52127a"

#client ID and Client Secret for Spotify API
client_id = '8e2db28f21e749d797722f5dc351e65a'
client_secret = '38269d3f577d4c34a67e2b2978f8a9e6'


spotify_client = SpotifyClient(client_id, client_secret, port=5000) #create an instance of the SpotifyClient class with the provided credentials


auth = Blueprint('auth', __name__) #create a Blueprint named 'auth' to define authentication routes

@auth.route('/linker', methods=['GET', 'POST']) #route to handle linking user's music streaming accounts
@login_required
def linker():
    if request.method == 'POST': 
        button_clicked = request.form.get('button_clicked')

        if button_clicked == 'spotify': #spotify login
            auth_url = spotify_client.get_auth_url() #set redirect url to spotify login
            return redirect(auth_url) 
        
        if button_clicked == 'soundcloud': #soundcloud login
            if 'soundcloud_data' in request.form:
                soundcloud_data = request.form.get('soundcloud_data') #get soundcloud user id
                current_user.sound_c = soundcloud_data #set user id 
                db.session.commit()
                #flash(current_user.sound_c, category='success')
                return redirect(url_for('views.home')) #redirect to home

            return render_template("soundcloud_input.html", user=current_user)

    return render_template("linker.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST']) #route to handle user login
def login():
    if request.method == 'POST': #if login attempted
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): #if login successful
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.linker')) #redirect to linker
            else: #if login fails
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user) #stay at login



@auth.route('/logout') #route to handle user logout
@login_required 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/callback/q') #route to handle the callback from Spotify after successful authorization
def spotify_callback():
    # Extract the authorization code from the query parameters
    auth_token = request.args.get('code')

    # Get the authorization data and set the authorization_header
    spotify_client.get_authorization(auth_token)
    authorization_header = spotify_client.authorization_header

    # Store the authorization_header in the session
    session['authorization_header'] = authorization_header

    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST']) #route to handle user sign-up
def sign_up():
    if request.method == 'POST': #if sign up attempted
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif first_name is not None and len(first_name) < 1:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else: #create a new User object and add it to the database
            new_user = User(email=email, first_name=first_name, sound_c=None, password=generate_password_hash(password1, method='sha256')) 
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user) #stay at sign up







