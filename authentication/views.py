from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
#from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login,logout as user_logout
from django.views.decorators.csrf import csrf_protect
User=get_user_model()
#import authentication
# Create your views here.
# def signup_view(request):
#     return render(request, 'authentication/hackfake.html')
@csrf_protect
def signup(request):
    print("hello")
    print("entered signup")
    if request.method == 'POST':
        print("hello entered signup post")
        # Get all fields from POST data
        username = request.POST.get('username')

        if not username:
            # If username is not provided, return an error response
            context = {'username_not_set': True}
            return render(request, 'authentication/hackfake.html', context)

        # Get other fields
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not password:
          print("hello")
          context = {'password_empty': True}
          return render(request, 'authentication/hackfake.html', context)
        if password != confirm_password:
            context = {'passwords_not_equal': True}
            return render(request, 'authentication/hackfake.html', context)

        # Create user
        user = User.objects.create_user(username=username, password=password, email=email, age=age, gender=gender, phone_number=phone_number)
        # Perform further processing as needed
        return redirect('login')

    return render(request, "authentication/hackfake.html")
  
def login(request):
    print("hello login")
    if request.method == 'POST':
        print("hello login post")
        # Get the username and password from the POST data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, log them in
            auth_login(request, user)
            # Redirect to a success page or dashboard
            return redirect('/')  # Change 'dashboard' to the actual URL name of your dashboard view
        else:
            # Authentication failed, show an error message
            context = {'invalid_credentials': True}
            return render(request, 'authentication/hackfake.html', context)

    return render(request, 'authentication/hackfake.html')
def logout(request):
  user_logout(request)
  return redirect('/')