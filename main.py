import sqlite3
import os
from datetime import datetime
from flask import Flask,jsonify
app = Flask(__name__)
users = {} #where the key is the email and the value is a list that contains the username, the password of a user and list of trips
trips = {} # the key is the trip name and the value is an array that contains destination, total_cost, saving_plan, travel_date, saved_amount, to_save
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
    #check if email already exists
    if email in users:
        return "Email already exists"
    #else we create a new user with an empty list of trips
    #TODO Encrypt the password before saving the user
    users[email] = [username, password, []]
    return jsonify(users[email])

@app.route("/print_users")
def printUsers():
    #prints all current users
    return jsonify(users)

@app.route("/login/<email>/<password>")
def login(email, password):
    """lookup for the email in our users dict and check if password is right"""
    if email not in users:
        return "Email does not exist"
    elif password == users[email][1]: 
        #TODO create and return access token to authenticate requests
        return "Successfull login in"
    else:
        return "Incorrect password"
    

@app.route("/create_new_trip/<email>/<trip_name>/<total_cost>/<destination>/<saving_plan>/<travel_date>")
def newTrip(email,trip_name, destination, total_cost, saving_plan, travel_date):
    
    if email not in users:
        return "Email does not exist"
    elif trip_name in users[email][2]:
        return "Trip already exists, please choose a different name"
    
    users[email][2].append(trip_name) #adding trip to list of trips in users 
    #creating a trip with all the information required
    trip_name = trip_name + email #making trip unique
    
    now = datetime.now()
    #save the travel_date as an object
    splitted_date = travel_date.split('-');
    travel_date = datetime(int(splitted_date[0]), int(splitted_date[1]), int(splitted_date[2]))
    total_time = travel_date - now
    days_in_month = 30
    days_in_year = 365
    
    if saving_plan == "monthly":
        to_save = int(total_cost) / total_time.days * days_in_month
    elif saving_plan == "daily":
        to_save = int(total_cost) / total_time.days
        print(total_time.days)
    elif saving_plan == "yearly":
    #TODO if future date is less than a year from now there is a bug 
        to_save = int(total_cost) / total_time.days * days_in_year
    
    trips[trip_name] = [destination, total_cost, saving_plan, travel_date, 0, to_save] 
    return "Successfully created your trip, you will need to save %.2f %s" % (to_save, saving_plan)

@app.route("/list/<email>")
def list_trips(email): #Print all the trips of the user
    if email not in users:
        return "Email doesn't exist, please try again"
    return jsonify(users[email][2])

@app.route("/delete_trip/<email>/<trip_name>")
def delete_trip(email, trip_name): 
    if email not in users:
        return "Email doesn't exist, please try again"
    #first we will look if the trip exists
    if trip_name + email not in trips:
        return "The trips you are trying to delete doesn't exist, try with a different trip"
    #then if the trip exists we delete it first from trips and then from our trip list in users
    del trips[trip_name + email]
    users[email][2].remove(trip_name)
    return "Trip successfully removed"

@app.route("/edit_trip/<email>/<changing_parameter>/<new_value>")
def edit_trip(email, trip_name):
    
    return "User is editing one of the tips"

if __name__ == '__main__':
    app.run()
