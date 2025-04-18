from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    source = request.form['source']
    destination = request.form['destination']
    travel_time_str = request.form['travel_time']
    travel_time = datetime.strptime(travel_time_str, "%H:%M")

    # Simulated bus data
    bus_schedule = [
        {
            "transport": "Bus",
            "bus_name": "TNSTC Express",
            "route": f"{source} to {destination}",
            "departure_time": (travel_time + timedelta(minutes=15)).strftime("%I:%M %p"),
            "arrival_time": (travel_time + timedelta(hours=2)).strftime("%I:%M %p"),
            "cost": "₹80"
        },
        {
            "transport": "Bus",
            "bus_name": "SETC AC Bus",
            "route": f"{source} to {destination}",
            "departure_time": (travel_time + timedelta(minutes=45)).strftime("%I:%M %p"),
            "arrival_time": (travel_time + timedelta(hours=2, minutes=30)).strftime("%I:%M %p"),
            "cost": "₹150"
        }
    ]

    # Simulated train data (realistic Tamil Nadu train examples)
    train_schedule = [
        {
            "transport": "Train",
            "train_type": "Superfast",
            "train_name": "Vaigai Express",
            "route": "Madurai to Chennai",
            "departure_station": "Madurai Junction",
            "arrival_station": "Chennai Egmore",
            "departure_time": "06:40 AM",
            "arrival_time": "01:10 PM",
            "cost": "₹145"
        },
        {
            "transport": "Train",
            "train_type": "Express",
            "train_name": "Ananthapuri Express",
            "route": "Chennai to Nagercoil",
            "departure_station": "Chennai Egmore",
            "arrival_station": "Nagercoil Junction",
            "departure_time": "05:15 PM",
            "arrival_time": "07:30 AM",
            "cost": "₹240"
        },
        {
            "transport": "Train",
            "train_type": "Superfast",
            "train_name": "Pandian Express",
            "route": "Madurai to Chennai",
            "departure_station": "Madurai Junction",
            "arrival_station": "Chennai Egmore",
            "departure_time": "09:15 PM",
            "arrival_time": "05:10 AM",
            "cost": "₹175"
        }
    ]

    return jsonify({"routes": bus_schedule + train_schedule})


if __name__ == '__main__':
    app.run(debug=True)
