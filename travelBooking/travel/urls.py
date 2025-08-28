from django.urls import path,include
from . import views
urlpatterns=[
    path("",views.CreateTravel,name='new_travel'),
    path("filter/",views.searchTravels,name='filters_search'),
    path("places/",views.getAllPlaces,name='places')
]