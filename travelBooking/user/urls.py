from django.urls import path,include
from .views import signup,profile,profile,editProfile,logout_user
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("accounts/signup/",signup,name='user_accounts_signup'),
    path("profile/",profile,name='user_profile'),
    path("profile/edit",editProfile,name='user_profile_edit'),
    path("accounts/",include('django.contrib.auth.urls'))

]