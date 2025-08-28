from django.urls import path
from .views import UserBooking,getUserBookingById,cancelBooking
urlpatterns = [
    path("",UserBooking,name='user_booking'),
    path("history/<int:user_id>/",getUserBookingById,name='booking_history'),
    path("cancel/<int:booking_id>",cancelBooking,name='booking_cancel')
]