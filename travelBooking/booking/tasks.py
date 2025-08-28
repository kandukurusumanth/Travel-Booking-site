from celery import shared_task
from datetime import datetime
from .models import Booking

@shared_task
def expire_bookings():
    now = datetime.now()
    expired_bookings = Booking.objects.filter(status='CONFIRMED',travel__bookingDateAndTime__lte=now)
    for booking in expired_bookings:
        booking.status = 'CONFIRMED'
        booking.save()
