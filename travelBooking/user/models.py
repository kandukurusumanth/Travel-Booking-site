from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    profileId = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    
