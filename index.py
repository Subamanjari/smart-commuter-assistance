from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to handle cross-origin issues
from geopy.distance import geodesic
import datetime
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS to avoid cross-origin issues

# Estimated bus speed in km/h
BUS_SPEED = 40

# Dictionary of Tamil Nadu cities with their latitude and longitude
CITY_COORDINATES = {
    "chennai": (13.0827, 80.2707), "coimbatore": (11.0168, 76.9558),
    "madurai": (9.9252, 78.1198), "trichy": (10.7905, 78.7047),
    "salem": (11.6643, 78.1460), "tiruppur": (11.1085, 77.3411),
    "karur": (10.9601, 78.0766), "erode": (11.3410, 77.7172),
    "vellore": (12.9165, 79.1325), "thanjavur": (10.7867, 79.1378),
    "thoothukudi": (8.7642, 78.1348), "kanyakumari": (8.0883, 77.5385),
    "tirunelveli": (8.7139, 77.7567), "dindigul": (10.3667, 77.9700),
    "namakkal": (11.2194, 78.1674)
}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Commuter Assistance</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; padding: 20px; }
        h1 { color: #2c3e50; }
        input, button { padding: 10px; margin: 5px; width: 80%; max-width: 300px; border-radius: 5px; border: 1px solid #ccc; }
        button { background-color: #3498db; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #2980b9; }
        #results { margin-top: 20px; padding: 20px; background: white; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>Smart Commuter Assistance</h1>
    <form id="searchForm">
        <input type="text" id="location" placeholder="Enter your location" required>
        <input type="text" id="destination" placeholder="Enter your destination" required>
        <input type="time" id="departure_time" required>
        <button type="submit">Find Buses</button>
    </form>
    <div id="results"></div>
    <script>
        document.getElementById("searchForm").addEventListener("submit", function(event) {
            event.preventDefault();
            let location = document.getElementById("location").value;
            let destination = document.getElementById("destination").value;
            let departure_time = document.getElementById("departure_time").value;
            fetch("/search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ location: location, destination: destination, departure_time: departure_time })
            })
            .then(response => response.json())
            .then(data => {
                let resultsDiv = document.getElementById("results");
                resultsDiv.innerHTML = "<h2>Available Buses:</h2>";
                if (data.routes.length === 0) {
                    resultsDiv.innerHTML += "<p>No buses available for this route.</p>";
                } else {
                    data.routes.forEach(route => {
                        resultsDiv.innerHTML += `<p><strong>${route.bus_type} Bus</strong> - Route: ${route.route}, Departure Time: ${route.departure_time}, Arrival Time: ${route.arrival_time}, Cost: ${route.cost}</p>`;
                    });
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    location = data.get('location', '').strip().lower()
    destination = data.get('destination', '').strip().lower()
    departure_time = data.get('departure_time', '')
    
    if location not in CITY_COORDINATES or destination not in CITY_COORDINATES:
        return jsonify({"error": "Invalid location. Please enter a valid Tamil Nadu city."})
    
    distance = geodesic(CITY_COORDINATES[location], CITY_COORDINATES[destination]).km
    travel_time_hours = distance / BUS_SPEED
    travel_time_minutes = round(travel_time_hours * 60)
    
    departure_datetime = datetime.datetime.strptime(departure_time, '%H:%M')
    arrival_datetime = departure_datetime + datetime.timedelta(minutes=travel_time_minutes)
    
    bus_schedule = []
    for i in range(5):  # Generate 5 different bus options dynamically
        time_offset = i * 30  # Buses at 30 min intervals
        new_departure = departure_datetime + datetime.timedelta(minutes=time_offset)
        new_arrival = new_departure + datetime.timedelta(minutes=travel_time_minutes)
        
        bus_schedule.append({
            "bus_type": "Government" if i % 2 == 0 else "Private", 
            "route": f"{location.title()} to {destination.title()}", 
            "time": f"{travel_time_minutes} mins", 
            "departure_time": new_departure.strftime('%I:%M %p'), 
            "arrival_time": new_arrival.strftime('%I:%M %p'),
            "cost": f"₹{round(distance * (0.8 if i % 2 == 0 else 1.2))}"
        })
    
    return jsonify({"routes": bus_schedule})

if __name__ == '__main__':
    app.run(debug=True)
