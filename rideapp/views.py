from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Ride
from .serializers import UserSerializer, RideSerializer,CustomTokenObtainPairSerializer
from .utils import haversine, simulate_ride, SIMULATION_ACTIVE
import threading

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_location(self, request, pk=None):
        user = self.get_object()
        user.latitude = request.data.get('latitude')
        user.longitude = request.data.get('longitude')
        user.save()
        return Response({'status': 'User location updated'})

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        rider = request.user

        if rider.is_driver:
            return Response({'error': 'You can’t create rides with a driver account.'}, status=status.HTTP_400_BAD_REQUEST)

        drivers = User.objects.filter(is_driver=True, latitude__isnull=False, longitude__isnull=False)
        nearby_drivers = []

        for driver in drivers:
            dist = haversine(
                float(data['pickup_latitude']),
                float(data['pickup_longitude']),
                driver.latitude,
                driver.longitude
            )
            if dist <= 5:
                nearby_drivers.append((driver, dist))

        nearby_drivers = sorted(nearby_drivers, key=lambda x: x[1])[:3]

        if not nearby_drivers:
            return Response({'error': 'No nearby drivers available'}, status=status.HTTP_400_BAD_REQUEST)

        ride = Ride.objects.create(
            rider=rider,
            pickup_lat=data['pickup_latitude'],
            pickup_lng=data['pickup_longitude'],
            dropoff_lat=data['dropoff_latitude'],
            dropoff_lng=data['dropoff_longitude'],
            
        )

        # Add candidate drivers
        for driver, _ in nearby_drivers:
            ride.candidate_drivers.add(driver)

        return Response(RideSerializer(ride).data)

    @action(detail=True, methods=['patch'])
    def update_location(self, request, pk=None):
        ride = self.get_object()
        ride.current_lat = request.data.get('current_lat')
        ride.current_lng = request.data.get('current_lng')
        ride.save()
        return Response({'status': 'Ride location updated'})
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def accept_ride(self, request, pk=None):
        ride = self.get_object()
        user = request.user

        if not user.is_driver:
            return Response({'error': 'Only drivers can accept rides.'}, status=status.HTTP_403_FORBIDDEN)

        if ride.driver:
            return Response({'error': 'Ride already accepted by another driver.'}, status=status.HTTP_400_BAD_REQUEST)

        if user not in ride.candidate_drivers.all():
            return Response({'error': 'You are not eligible to accept this ride.'}, status=status.HTTP_403_FORBIDDEN)

        # Accept ride
        ride.driver = user
        ride.status = 'accepted'
        ride.candidate_drivers.clear()
        ride.save()

        return Response({'status': f'Ride accepted by {user.username}'})


    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        ride = self.get_object()
        new_status = request.data.get('status')
        ride.status = new_status
        ride.save()

        if new_status == 'started':
            SIMULATION_ACTIVE[ride.id] = True
            thread = threading.Thread(target=simulate_ride, args=(ride.id,))
            thread.start()
        elif new_status == 'completed':
            SIMULATION_ACTIVE[ride.id] = False

        return Response({'status': f'Ride status updated to {new_status}'})
