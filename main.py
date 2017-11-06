from flask import Flask
app = Flask(__name__)

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
