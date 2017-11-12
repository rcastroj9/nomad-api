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

@app.route("/print_trips")
def printTrips():
    #pritns all trips 
    return jsonify(trips)

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
    
def calc_to_save(total_cost, saving_plan, travel_date, saved_amount):
    now = datetime.now()
    splitted_date = travel_date.split('-');
    #save the travel_date as an object
    travel_date = datetime(int(splitted_date[0]), int(splitted_date[1]), int(splitted_date[2]))
    total_time = travel_date - now
    days_in_month = 30
    days_in_year = 365
    total_cost -= saved_amount
    
    if saving_plan == "monthly":
        to_save = int(total_cost) / total_time.days * days_in_month
    elif saving_plan == "daily":
        to_save = int(total_cost) / total_time.days
        print(total_time.days)
    elif saving_plan == "yearly":
    #TODO if future date is less than a year from now there is a bug 
        to_save = int(total_cost) / total_time.days * days_in_year    
    return to_save
    


@app.route("/create_new_trip/<email>/<trip_name>/<total_cost>/<destination>/<saving_plan>/<travel_date>")
def newTrip(email,trip_name, destination, total_cost, saving_plan, travel_date):
    
    if email not in users:
        return "Email does not exist"
    elif trip_name in users[email][2]:
        return "Trip already exists, please choose a different name"
    
    users[email][2].append(trip_name) #adding trip to list of trips in users 
    #creating a trip with all the information required
    trip_name = trip_name + email #making trip unique
    #use helper function to calculate how much is necessary to save per saving_plan
    saved_amount = 0
    to_save = calc_to_save(total_cost, saving_plan, travel_date, saved_amount)
    
    trips[trip_name] = [destination, total_cost, saving_plan, travel_date, saved_amount, to_save] 
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

@app.route("/edit_trip/<email>/<trip_name>/<changing_param>/<new_value>")
def edit_trip(email, trip_name, changing_param, new_value):
    #check if the trip the user wants to edit exists
    if trip_name not in users: 
        return "Trip does not exists, please try with a different one"
    #trip name
    if changing_param == "name": #change it in the users DS as well as in the trips structure
        trip_list = users[email][2]
        index = trip_list.index(trip_name)
        trip_list[index] = new_value
        #now we change the name trip in the trips DS
        trips[new_value + email] = trips.pop(trip_name + email)
        return "Successfully updated trip name"
    #date
    elif changing_param == "date":
        #change date in trip DS only
        splitted_value = new_value.split('-')
        new_value = datetime(splitted_value[0], splitted_value[1], splitted_value[2])
        trips[trip_name][3] = new_value
        trips[trip_name][5] = calc_to_save(trips[trip_name][1], trips[trip_name][2], trips[trip_name][3], trips[trip_name[4])
        return "Successfully updated date now, you will have to save %.2f %s" % to_save, saving_plan
    #saving_plan
    elif changing_param == "saving plan":
        #change saving plan in trip DS only 
        trips[trip_name][2] = new_value
        trips[trip_name][5] = calc_to_save(trips[trip_name][1], trips[trip_name][2], trips[trip_name][3], trips[trip_name[4])
        return "Successfully updated saving plan now, you will have to save %.2f %s" % to_save, saving_plan
    #cost
    elif changing_param == "cost":
        trips[trip_name][1] = new_value
        trips[trip_name][5] = calc_to_save(trips[trip_name][1], trips[trip_name][2], trips[trip_name][3], trips[trip_name[4])
        return "Successfully updated cost of trip now, you will have to save %.2f %s" % to_save, saving_plan
    #amount saved
    elif changing_param == "amount saved":
        trips[trip_name][4] = new_value
        trips[trip_name][5] = calc_to_save(trips[trip_name][1], trips[trip_name][2], trips[trip_name][3], trips[trip_name[4])
        return "Successfully updated you amount saved until now, you wil have to save  %.2f %s" % to_save, saving_plan

@app.
if __name__ == '__main__':
    app.run()
