from flask import request, render_template
import requests
from app.forms import LoginForm
from app import app

@app.route("/")
def hello_world():
    return "<p>Hello, Thieves!</p>"


@app.route('/home')
def home():
    return '<h1>This is the home page</h1>'

@app.route('/user/<username>')
def username(username):
    return f'Hello {username}!'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

REGISTERED_USERS = {
    'dylank@thieves.com': {
        'name': 'Dylan',
        'password': 'ilovemydog'
    }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in REGISTERED_USERS and password == REGISTERED_USERS[email]['password']:
            return f"Hello, {REGISTERED_USERS[email]['name']}"
        else:
            return 'Invalid email or password'
    else:
        print('not validated')
        return render_template('login.html', form=form)
    
@app.route('/students')
def students():
    students_lst = ['Gabe', 'Will', 'Sean', 'Peace']
    return render_template('students.html', students_lst=students_lst)

@app.route('/ergast', methods=['GET', 'POST'])
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