from flask import request, render_template, redirect, url_for, flash
import requests
from app.forms import LoginForm, SignUpForm
from app import app, db
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html')


    
@app.route('/students')
@login_required
def students():
    students_lst = ['Gabe', 'Will', 'Sean', 'Peace']
    return render_template('students.html', students_lst=students_lst)

@app.route('/ergast', methods=['GET', 'POST'])
@login_required
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        rnd = request.form.get('rnd')
        
        url = f'http://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
        response = requests.get(url)
        if response.ok:
            try:
                standings_data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
                driver_data = get_driver_info(standings_data)
                return render_template('ergast.html', driver_data=driver_data)
            except IndexError:
                return 'That year or round does not exist!'
    return render_template('ergast.html')

# Helper Function
def get_driver_info(data):
    new_driver_data = []
    for driver in data:
        driver_dict = {
            'full_name': f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}",
            'DOB': driver['Driver']['dateOfBirth'],
            'wins': driver['wins'],
            'team': driver['Constructors'][0]['name']
        }
        if len(new_driver_data) <= 5:
            new_driver_data.append(driver_dict)
    return new_driver_data

# AUTHENTICATION
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Welcome back {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', form=form, error=error)
    else:
        print('not validated')
        return render_template('login.html', form=form)
    
# SIGN UP FORM
@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        # This data is coming from the signup form
        user_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data.lower(),
            'password': form.password.data
        }

        # Create user instance
        new_user = User()

        # Set user_data to our User attributes
        new_user.from_dict(user_data)

        # save to database
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you for signing up {user_data["first_name"]}!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out!', 'warning')
    return redirect(url_for('home'))