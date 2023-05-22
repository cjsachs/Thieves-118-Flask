from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Routing
@app.route('/thieves')
def thieves():
    return 'Thieves-118 is the best cohort EVAAAA!'

# Variable Rules
@app.route('/thieves/user/<username>')
def user_profile(username):
    return f'User {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'

# HTTP Methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Logged IN'
    else:
        return render_template('login.html')


# Rendering Templates
@app.route('/students')
def students():
    students = ['student 1', 'student 2', 'student 3']
    return render_template('home.html', students=students)

# Ergast F1 API Route
@app.route('/ergast', methods=['GET', 'POST'])
def ergast():
    if request.method == 'POST':
        # Fetching Values from our form
        year = request.form.get('year')
        rnd = request.form.get('rnd')
        print(year, rnd)

        # Our API
        url = f'http://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
        response = requests.get(url)
        if response.ok:
            try:
                standings_data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
                drivers_data = get_driver_info(standings_data)
                return render_template('ergast.html', drivers_data=drivers_data)
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