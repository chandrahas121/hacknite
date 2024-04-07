from django.shortcuts import render, redirect
from .models import UserTrip
from datetime import datetime
from django.db.models import Q
from ride.models import Rating
def home(request):
    return render(request, 'hacnitewelcome.html')

def profile(request):
    return render(request, 'hackniteprofile.html')

from django.contrib import messages

def search_users(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if source and destination and date and time:
            input_time = datetime.strptime(time, '%H:%M').time()
            current_user = request.user
            
            # Save the user's trip details to the database
            user_trip = UserTrip.objects.create(user=current_user, source=source, destination=destination, date=date, time=input_time)
            user_trip.save()
            # Query UserTrip objects with the same source, destination, and date
            users_with_same_trip = UserTrip.objects.filter(~Q(user=current_user), source=source, destination=destination, date=date)
            
           
            # Sort the queryset based on the time difference between the input time and other users' times
        
            sorted_users = sorted(users_with_same_trip, key=lambda trip: abs((datetime.combine(datetime.strptime(date, '%Y-%m-%d').date(), input_time) - datetime.combine(trip.date, trip.time)).total_seconds()))

            context = {'users_with_same_trip': sorted_users}
            print(context)
            return render(request, 'hacknitesearched1.html', context)
        else:
            # Use Django's messages framework to display an error message
            messages.error(request, 'Please provide valid search criteria.')
            return redirect('/')
    else:
        return render(request, 'hacnitewelcome.html')  # Render home page for other request methods