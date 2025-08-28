from django.shortcuts import render,redirect
from .form import UserRegisterForm,ProfileForm,UserForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout
from .models import Profile
from django.contrib import messages
from travelBooking.responses import success,error
def signup(request):
    if request.method == "POST":
        try:
            form = UserRegisterForm(request.POST)
            print(form, "this is the form")
            if form.is_valid():
                form.save()
                messages.success(request,"Account created successfully!")
                return redirect("/")
            else:
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            error['error'] = str(e)
            return JsonResponse(error,status=500)

    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})
@login_required
def profile(request):
    try:
        user = request.user
        profile = getattr(user, 'profile', None)
        return render(request, 'registration/userProfile.html', {
            'user': user,
            'profile': profile
        })
    except Exception as e:
        messages.error(request, f"Error loading profile: {str(e)}")
        return redirect('/')  
@login_required
def editProfile(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('/user/profile')  
            except Exception as e:
                messages.error(request,"something went wrong while saving data")

        else:
            messages.error(request, "Please correct the errors below")
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'registration/editProfile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    
def logout_user(req):
    logout(req)
    return redirect("/")