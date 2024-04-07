from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
#from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login,logout as user_logout
from django.views.decorators.csrf import csrf_protect
import re
from django.contrib import messages
User=get_user_model()
#import authentication
# Create your views here.
# def signup_view(request):
#     return render(request, 'authentication/hackfake.html')


def is_strong_password(password):
    """
    Function to check if the password meets the strength criteria.
    Returns True if the password is strong, False otherwise.
    """
    # Define strength criteria (e.g., minimum length, presence of uppercase, lowercase, digits, and special characters)
    min_length = 8
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special_char = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    # Check if the password meets all criteria
    return (
        len(password) >= min_length and
        has_uppercase and
        has_lowercase and
        has_digit and
        has_special_char
    )

@csrf_protect
def signup(request):
    print("hello")
    print("entered signup")
    if request.method == 'POST':
        print("hello entered signup post")
        # Get all fields from POST data
        username = request.POST.get('username')
        # Get other fields
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([username, gender, age, email, phone_number, password, confirm_password]):
            context = {'fields_empty': True}
            return render(request, 'authentication/hackfake.html', context)
        
        if password != confirm_password:
            context = {'passwords_not_equal': True}
            return render(request, 'authentication/hackfake.html', context)
        
        # Check if the password is strong
        if not is_strong_password(password):
            context = {'weak_password': True}
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

        if not username or not password:
            if not username:
                messages.error(request, 'Username field is empty.')
            if not password:
                messages.error(request, 'Password field is empty.')
            return render(request, 'authentication/hackfake.html')
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