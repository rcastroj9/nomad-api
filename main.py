import sqlite3
import os
from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__) # loading configuration from this file 

#Initializing the database
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'information.db'),
    SECRET_KEY = 'development key',
    USERNAME='admin',
    PASSWORD='mysecretpassword'
    ))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.route("/monitor")
def monitor():
    return "Server is working!"

@app.route("/signup/<username>/<email>/<password>")
def signUp(username, email, password):
    return "Username trying to signup"

@app.route("/login/<email>/<password>")
def login(email, password):
    return "Username login in"

@app.route("/create_new_trip/<email>/<cost>/<destination>/<saving_plan>/<travel_date>")
def newTrip(destination, cost, saving_plan, travel_date):
    return "User creating a new trip"

@app.route("/list/<email>")
def list_trips(email):
    return "Lists all trip of User"

@app.route("/delete_trip/<email>/<trip_name>")
def delete_trip(email, trip_name):
    return "User is deleting one of the trips"

@app.route("/edit_trip/<email>/<trip_name>")
def edit_trip(email, trip_name):
    return "User is editing one of the tips"

if __name__ == '__main__':
    app.run()
