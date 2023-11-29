from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
# A way to secure a password. Not in plain text. 
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
# This module import below will be used to show users login to be only displayed home and signout tab. Rather than others or for ppl not signed in to have access to the home page. 
# Usermixin in models.py go in hand with current_user
from flask_login import login_user, login_required, logout_user, current_user


# A hashing function is a function that has no inverse

auth = Blueprint('auth', __name__)

# We don't want to show html cotenet/return but return templates(html pages)
# Now an example of how to pass a variable to say login through our backend here. Can pass multiple variables. Now we can access it in the html pages.
# When we hit some function, route, endpoints ,etc. In our case is login, logout, etc. Now these route need to know if we sent a post, get, request, etc. 
#   Based on the request they will do something differently. 
#       Get request typically means loading a webpage, retrieving information. In this case retrieving an html that represents that page. 
#       Post request usually means a change to a database, state of the website or system. 
#           Updating or creating something. 

# Now we are going to make sure that login and sign up are able to accept post request
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Now we will check if the email is valid and in the database. 
        # Below is for looking a specific user or entry...
        user = User.query.filter_by(email=email).first()
        if user:
            # user meaning here in the def above and using the password recieived from post. Then comparing it with the actual password. 
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                # The remember=true will ensure the user can stay login so they don't resign again. Unless session cleared or history
                login_user(user, remember=True)
                # When yes then redirect to the home page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    """
    # Now to get the information that we sent to this form we type:(below) 
    data = request.form # URL, method, all info
    print(data) # Issue here is we didn't differentiate between the get and post request. Only give data if we send form. if we reload it just sends a get request and so...
    """
    return render_template("login.html", user=current_user)

# Added decorator at login_required so only can be accessed if you are logged in. 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Now how to get user information and store it in the database and create the user account. 
    # How to differentiate 
    if request.method == 'POST':
        # The method .get() to get a specific attribute or value 
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # make sure we are not signing up user with same email. 
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist.', category='error')

        # Now some validation check. Whether to create an account or not. 
        # Now to alert users if one of the criteria is not met we can do 'message flashing'. 'import flash
        # Now to actually display the messages go to the base.htlm file and create a with and inside a for loop to go through all message. There could be multiple.
        elif len(email) < 4: 
            flash('Email must be greater than 3 characters.', category='error')
            
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
            
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            
        else:
            # sha2356 is just hashing algorithm. Changed it to the current due to 'not valid hash method'
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256:6000'))
            # add the new user to the database 
            db.session.add(new_user)
            # To update the database
            db.session.commit()
            # Included here since they should be logged in when signed up.
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            # add user to database 
            # Return and redirect to another page
            return redirect(url_for('views.home'))
           
    return render_template("sign_up.html", user=current_user)


# Stopped at 1:55:55
