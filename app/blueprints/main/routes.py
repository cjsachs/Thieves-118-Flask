from flask import request, render_template
import requests
from . import main
from flask_login import login_required, current_user
from app.models import Post, User

@main.route("/")
@main.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts[::-1])


    
@main.route('/students')
@login_required
def students():
    students_lst = ['Gabe', 'Will', 'Sean', 'Peace']
    return render_template('students.html', students_lst=students_lst)

@main.route('/ergast', methods=['GET', 'POST'])
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

@main.route('/contact')
@login_required
def contacts():
    users = User.query.all()
    for user in users:
        if user in current_user.followed:
            user.isFollowing = True
    return render_template('contacts.html', users=users)
