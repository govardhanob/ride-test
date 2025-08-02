from rest_framework import serializers
from .models import User, Ride
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)

    def validate(self, attrs):
        # Validate username & password
        data = super().validate(attrs)

        # Update latitude and longitude
        user = self.user
        user.latitude = attrs['latitude']
        user.longitude = attrs['longitude']
        user.save()

        # Add user info to token response if needed
        data.update({
            'user_id': user.id,
            'username': user.username,
            'is_driver': user.is_driver,
            'latitude': user.latitude,
            'longitude': user.longitude
        })

        return data


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[('driver', 'Driver'), ('rider', 'Rider')], write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_driver', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_driver': {'read_only': True}
        }

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.is_driver = (role == 'driver')
        user.save()
        return user
        
class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ('rider', 'driver', 'status', 'current_lat', 'current_lng')
