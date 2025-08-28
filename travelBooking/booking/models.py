from django.db import models
from django.contrib.auth.models import User
class Booking(models.Model):
    bookingId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    travel = models.ForeignKey('travel.Travel',on_delete=models.CASCADE)
    numberOfSeatsBooked = models.IntegerField(default=1) 
    totalPrice = models.FloatField()
    bookingDate = models.DateTimeField()
    status = models.CharField(max_length=10,choices=[("CONFIRMED","✅ CONFIRMED"),("CANCELLED","❌ CANCELLED")],default="CANCELLED")
    
