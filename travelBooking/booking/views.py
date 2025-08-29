from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from django.utils import timezone
from travelBooking.travel.models import Travel
from . import models
from django.forms.models import model_to_dict
from travelBooking.responses import success,error
from django.contrib.auth.decorators import login_required
def UserBooking(request):
    if request.method == "POST":
        try:
            if request.content_type != "application/json":
                error['error']="Expected application/json"
                return JsonResponse(error, status=400)
            with transaction.atomic():
                data = json.loads(request.body.decode('utf-8'))
                bookingseats = data.get("numberOfSeatsBooked")
                travel_id = data.get("travel_id")

                transportData = Travel.objects.select_for_update().get(pk=travel_id)
                if bookingseats<=0:
                    error['error'] = "0 seats can't be booked"
                    return JsonResponse(error,400)
                totalPrice = transportData.price * bookingseats
                if transportData.availableSeats < bookingseats:
                    models.Booking.objects.create(
                        **data,
                        totalPrice=totalPrice,
                        status="CANCELLED"
                    )
                    error["error"] = "booking failed"
                    return JsonResponse(error,status=400)
                transportData.availableSeats-=bookingseats
                transportData.save()
                currSeats = transportData.availableSeats
                confirmBooking = models.Booking.objects.create(**data,totalPrice=totalPrice,status='CONFIRMED')
                confirmBookingDict =[]
                if confirmBooking:
                    confirmBookingDict = model_to_dict(confirmBooking)
                    confirmBookingDict['reaminingSeats'] =currSeats
                    success["data"] = confirmBookingDict
                    return JsonResponse(success,status=201)
                error["error"] = "booking failed"
                return JsonResponse(error,status=400)
        except json.JSONDecodeError:
            error['error'] = "Invalid JSON"
            return JsonResponse(error, status=400)
        except Travel.DoesNotExist:
            error['error'] = "Travel not found"
            return JsonResponse(error, status=404)
        except Exception as e:
            error['error'] = str(e)
            return JsonResponse(error,status=500)
def getUserBookingById(request,user_id):
    if request.method == "GET":
        try:
        
            if not user_id:
                error['error'] = "Invalid input"
                return JsonResponse(error,status=400)
            userBookingModel = models.Booking.objects.select_related('travel','user').filter(user_id=user_id)
            userBookingDict = []
            for model in userBookingModel:
                bookingData = model_to_dict(model)
                bookingData['travel'] = model_to_dict(model.travel)
                bookingData['sourceplace'] = model_to_dict(model.travel.source)
                bookingData['destinationplace'] = model_to_dict(model.travel.destination)
                bookingData['user'] = model_to_dict(model.user)

                userBookingDict.append(bookingData)
            now = timezone.now()
            return render(request, "booking/bookingHistory.html", {"bookings": userBookingDict,"now":now})
        except models.Booking.DoesNotExist:
            error["error"] = "Booking not Found"
            return JsonResponse(error,status=404) 
        except Exception as e:
            error["error"] = str(e)
            return JsonResponse(error,status=500)

def cancelBooking(request,booking_id):
    if request.method == "PATCH":
        try:
            with transaction.atomic():
                if not booking_id:
                    error['error'] = "invalid input"
                    return JsonResponse(error,status=400)
                cancelBookingModel = models.Booking.objects.get(pk=booking_id)
                cancelBookingModel.status = "CANCELLED"
                cancelBookingModel.save()
                traveldata = cancelBookingModel.travel
                id = int(traveldata.travelId)
                travelinfo = Travel.objects.select_for_update().get(pk=id)
                bookedUserSeats = cancelBookingModel.numberOfSeatsBooked
                travelinfo.availableSeats += bookedUserSeats
                travelinfo.save()
                success['data'] = 'your booking is cancelled'
                return JsonResponse(success,status=204)
        except models.Booking.DoesNotExist:
            error['error'] = "Booking not found"
            return JsonResponse(error, status=404)
        except Travel.DoesNotExist:
            error['error'] = "Travel not found"
            return JsonResponse(error, status=404)
        except Exception as e:
            print(str(e),"this is the error")
            error['error'] = str(e)
            return JsonResponse(error, status=400)
        
