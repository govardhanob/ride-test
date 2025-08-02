from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_driver = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.username

class Ride(models.Model):
    rider = models.ForeignKey(User, related_name='rides', on_delete=models.CASCADE)
    driver = models.ForeignKey(User, related_name='drives', null=True, blank=True, on_delete=models.SET_NULL)
    candidate_drivers = models.ManyToManyField(User, related_name='candidate_rides', blank=True) 
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    dropoff_lat = models.FloatField()
    dropoff_lng = models.FloatField()
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('requested', 'requested'),
            ('accepted', 'accepted'),
            ('started', 'started'),
            ('completed', 'completed'),
            ('cancelled', 'cancelled')
        ],
        default='requested'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
