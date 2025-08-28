from django.db import models

class Places(models.Model):
    id = models.AutoField(primary_key=True)
    placeName = models.CharField(max_length=100)
class Travel(models.Model):
    travelId = models.AutoField(primary_key=True)
    travelType =  models.CharField(max_length=10,choices=[("FLIGHT" ,"FLIGHT"),("TRAIN" , "TRAIN"),("BUS" , "BUS")])
    source = models.ForeignKey(Places,on_delete=models.CASCADE,null=True,related_name='source_city')
    destination = models.ForeignKey(Places,on_delete=models.CASCADE,null=True,related_name='destination_city')
    bookingDateAndTime = models.DateTimeField()
    price = models.FloatField() 
    availableSeats = models.IntegerField()
    discount = models.FloatField(null=True)
   