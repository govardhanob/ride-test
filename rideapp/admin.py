from django.contrib import admin
from .models import User, Ride

admin.site.register(User)
admin.site.register(Ride) # Register the Ride model as well
# Register your models here.
