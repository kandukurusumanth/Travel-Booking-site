from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

from . import models
import json
from travelBooking.responses import success,error
def CreateTravel(request):
    if request.method == "POST":
        try:
            if request.content_type != "application/json":
                error['error']="Expected application/json"
                return JsonResponse(error, status=400)
            data = json.loads(request.body.decode("utf-8"))
            print(data,"this is the data")
            travel = models.Travel.objects.create(**data)
            travel_dict = model_to_dict(travel)
            return JsonResponse(travel_dict,status=201)
        except json.JSONDecodeError:
            error['error']="Invalid json"
            return JsonResponse(error,status=400)
        
        except Exception as e:
            error['error'] = str(e)
            return JsonResponse(error,staus=500)
def searchTravels(request):
    if request.method == "GET":
        try:
            source = request.GET.get("source")
            destination = request.GET.get("destination")
            dateAndTime = request.GET.get("date")
            if not(source or destination or dateAndTime):
                error['error']= "Invalid input"
                return JsonResponse(error,status=400)
            price = request.GET.get("price")
            date = request.GET.get("datesort")
            flighttype = request.GET.get("type")
            data = models.Travel.objects.select_related('source','destination').filter(source=source,destination=destination,bookingDateAndTime__gte=dateAndTime)
            print(data,"this is the data")
            if flighttype:
                data = data.filter(travelType=flighttype)
            if price:
                if price=="desc":
                    data = data.order_by('-price')
                else:
                    data = data.order_by('price')
            if date:
                if date =="desc":
                    data = data.order_by('-bookingDateAndTime')
                else:
                    data = data.order_by('bookingDateAndTime')
            dictdata = []
            for model in data:
                singledict=model_to_dict(model)
                singledict['sourceplace'] = model_to_dict(model.source)
                singledict['destinationplace'] = model_to_dict(model.destination)
                dictdata.append(singledict)
            success["data"] = dictdata
            print(success)
            if data:
                return JsonResponse(success,status=200)
        except models.Travel.DoesNotExist:
            error['error'] = "Travel not found"
            return JsonResponse(error,status=404)
        except Exception as e:
            print(str(e)  ,"this is the error")
            error['error'] = str(e)
            return JsonResponse(error,status=500)
def getAllPlaces(request):
    if request.method =="GET":
        try:
            
            allPlaces = models.Places.objects.all()
            print(allPlaces,"these are allplaces")
            if len(allPlaces)==0:
                error['error'] = "Places not found"
                return JsonResponse(error,status=404)
            placesDict = []
            for places in allPlaces:
                placeDict = model_to_dict(places)
                placesDict.append(placeDict)
            success['data'] = placesDict
            return JsonResponse(success,status=200)
        except Exception as e:
            error['error']= str(e)
            return JsonResponse(error,status=500)
        
@login_required(login_url='login')  
def home_view(request):
    return render(request, "travel/home.html")