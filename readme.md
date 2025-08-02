🚗 Ride Sharing API
A Django REST Framework based Ride Sharing API with JWT authentication. It supports registering users as drivers or riders, creating and accepting ride requests, live ride tracking, and ride simulations.

📦 Features
JWT-based authentication (djangorestframework-simplejwt)

Role-based access (driver or rider)

Nearby driver matching using the Haversine formula

Simulated rides with threading

Live location updates for rides and users

🧰 Setup Instructions

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
🔐 Authentication
🔑 JWT Login
Endpoint: POST /api/token/
Body:

json
Copy
Edit
{
  "username": "john",
  "password": "secret"
}
Response:

json
Copy
Edit
{
  "refresh": "token",
  "access": "token"
}
👤 User Registration
📌 POST /api/register/
Register a new user (either driver or rider).

Request Body:

json
Copy
Edit
{
  "username": "john",
  "password": "secret123",
  "is_driver": false,
  "latitude": 10.0,
  "longitude": 76.3
}
Response:

json
Copy
Edit
{
  "id": 1,
  "username": "john",
  "is_driver": false,
  "latitude": 10.0,
  "longitude": 76.3
}
📍 PATCH /api/register/{id}/update_location/
Update user’s current location (authenticated).

Request Header:

makefile
Copy
Edit
Authorization: Bearer <access_token>
Body:

json
Copy
Edit
{
  "latitude": 9.95,
  "longitude": 76.25
}
Response:

json
Copy
Edit
{
  "status": "User location updated"
}
🚕 Ride API
📌 POST /api/ride/
Create a ride request (only rider can create).

Request Header:

makefile
Copy
Edit
Authorization: Bearer <access_token>
Body:

json
Copy
Edit
{
  "pickup_latitude": 9.96,
  "pickup_longitude": 76.26,
  "dropoff_latitude": 9.98,
  "dropoff_longitude": 76.28
}
Logic:

Filters drivers within 5 km using haversine().

Assigns top 3 closest drivers to the ride.

Response:

json
Copy
Edit
{
  "id": 1,
  "rider": 2,
  "pickup_lat": 9.96,
  "pickup_lng": 76.26,
  "dropoff_lat": 9.98,
  "dropoff_lng": 76.28,
  "status": "pending",
  "candidate_drivers": [1, 3, 4]
}
📌 PATCH /api/ride/{id}/accept_ride/
Driver accepts a ride.

Request Header:

makefile
Copy
Edit
Authorization: Bearer <access_token>
Response:

json
Copy
Edit
{
  "status": "Ride accepted by driver_username"
}
📌 PATCH /api/ride/{id}/update_location/
Update the real-time location of the ride.

Body:

json
Copy
Edit
{
  "current_lat": 9.97,
  "current_lng": 76.27
}
Response:

json
Copy
Edit
{
  "status": "Ride location updated"
}
📌 PATCH /api/ride/{id}/update_status/
Update the ride status: pending, accepted, started, completed.

Request:

json
Copy
Edit
{
  "status": "started"
}
Logic:

On "started": starts simulation in a separate thread.

On "completed": stops simulation.

Response:

json
Copy
Edit
{
  "status": "Ride status updated to started"
}
🧠 Utility Functions (in utils.py)
🧭 haversine(lat1, lon1, lat2, lon2)
Calculates the distance (in km) between two coordinates using the Haversine formula.

🎮 simulate_ride(ride_id)
Simulates a live ride:

Periodically updates ride's current location.

Stops simulation when status changes to completed.

Global dictionary used:

python
Copy
Edit
SIMULATION_ACTIVE = {}  # ride_id: bool
🔑 Permissions
Endpoint	Role	Auth Required
POST /api/register/	Anyone	❌
POST /api/token/	Anyone	❌
PATCH /register/{id}/update_location/	Authenticated	✅
POST /ride/	Rider only	✅
PATCH /ride/{id}/accept_ride/	Driver only	✅
PATCH /ride/{id}/update_location/	Any ride user	✅
PATCH /ride/{id}/update_status/	Any ride user	✅

🔍 Sample Users
Rider
json
Copy
Edit
{
  "username": "rider1",
  "password": "pass123",
  "is_driver": false,
  "latitude": 10.01,
  "longitude": 76.33
}
Driver
json
Copy
Edit
{
  "username": "driver1",
  "password": "pass123",
  "is_driver": true,
  "latitude": 10.02,
  "longitude": 76.34
}
🧪 Testing Checklist
Test Case	Expected Result
Rider creates ride	3 nearby drivers assigned
Driver accepts ride	Ride assigned to that driver
Start ride	Simulation begins
Complete ride	Simulation ends
Unauthorized user creates ride	403 error
Rider tries to accept ride	403 error

🧱 Models (Simplified)
🚶‍♂️ User
username

password

is_driver

latitude

longitude

🚕 Ride
rider: FK(User)

driver: FK(User)

pickup_lat, pickup_lng

dropoff_lat, dropoff_lng

current_lat, current_lng

status: pending, accepted, started, completed

candidate_drivers: M2M(User)



