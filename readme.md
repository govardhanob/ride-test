
# Ride Sharing API

This is a basic ride sharing API built with Django Rest Framework that allows users to register as riders or drivers, log in, create ride requests, and simulate ride progression.

## Features

- User Registration and Login (JWT Auth)
- Location Update for Drivers
- Ride Request Creation by Riders
- Proximity-based Driver Matching (Haversine Formula)
- Ride Status Updates with Simulation
- Candidate Driver Selection and Ride Acceptance Flow

## Setup

<<<<<<< HEAD
1. Clone the repo:
```bash
git clone https://github.com/govardhanob/ride-test.git
cd ride-test
```

2. Create a virtual environment and activate it:
```bash
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
```

3. Install dependencies:
```bash
=======
🧰 Setup Instructions

>>>>>>> 1a17e435768e5e33981697a746ee5c557cb6fb23
pip install -r requirements.txt
```

4. Run the server:
```bash
python manage.py runserver
```

## Environment Setup

Make sure to create a `.env` file (if you're using one).

## API Endpoints

### 1. Register

```http
POST /api/register/
```

#### Example (For Rider or Driver)
```json
{
  "username": "rider1",
  "email": "rider1@example.com",
  "password": "yourpassword",
  "is_driver": false
}
```
```json
{
  "username": "driver1",
  "email": "driver1@example.com",
  "password": "yourpassword",
  "is_driver": true
}
```

> Note: Latitude and longitude are not passed during registration.

---

### 2. Login

```http
POST /api/login/
```

#### Example
```json
{
  "username": "rider1",
  "password": "yourpassword",
  "latitude": 10.54321,
  "longitude": 76.987654
}
```

Returns access and refresh tokens.

---

### 3. Update Driver Location after login

```http
PATCH /api/register/{id}/update_location/
Headers: Authorization: Bearer <your_token>
```

#### Example Body:
```json
{
  "latitude": 10.54321,
  "longitude": 76.987654
}
```

---

### 4. Create Ride Request (Rider only)

```http
POST /api/rides/
Headers: Authorization: Bearer <rider_token>
```

#### Example Body:
```json
{
  "pickup_latitude": 10.543,
  "pickup_longitude": 76.987,
  "dropoff_latitude": 10.545,
  "dropoff_longitude": 76.989
}
```

Returns ride details with a list of candidate drivers (maximum of 3 drivers) based on proximity.

**Candidate Driver Selection:**  
- Uses the Haversine formula to calculate distance from pickup location.
- Filters top 3 nearest available drivers.

---

### 5. Accept Ride (Driver only)

```http
PATCH /api/rides/{ride_id}/accept/
Headers: Authorization: Bearer <driver_token>
```

Assigns the driver to the ride if they are in the candidate list.

---

### 6. List All Rides (Anyone)

```http
GET /api/rides/
Headers: Authorization: Bearer <token>
```

---

### 7. Get Single Ride

```http
GET /api/rides/{id}/
Headers: Authorization: Bearer <token>
```

---

### 8. Update Ride Status (Driver only)

```http
PATCH /api/rides/{id}/
Headers: Authorization: Bearer <driver_token>
```

#### Example Body:
```json
{
  "status": "started"
}
```

**Simulation Logic:**  
- When the ride status is updated to `"started"`, a background thread begins simulating the ride.
- The rides current location is updated at intervals to reflect real-time movement.
- The ride status changes from `"started"`  → `"completed"` .
- Once completed, the thread stops itself.

---

## Author

Govardhan
