from math import radians, cos, sin, asin, sqrt
import time

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

SIMULATION_ACTIVE = {}

def simulate_ride(ride_id):
    from .models import Ride
    from django.db import connection
    while SIMULATION_ACTIVE.get(ride_id):
        ride = Ride.objects.get(id=ride_id)
        if ride.current_lat is None or ride.current_lng is None:
            ride.current_lat = ride.pickup_lat
            ride.current_lng = ride.pickup_lng
        else:
            ride.current_lat += (ride.dropoff_lat - ride.pickup_lat) / 10
            ride.current_lng += (ride.dropoff_lng - ride.pickup_lng) / 10
        ride.save()
        time.sleep(5)
        if ride.status == 'completed':
            SIMULATION_ACTIVE[ride_id] = False
    connection.close()
