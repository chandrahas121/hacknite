from authentication.models import CustomUser
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from .models import FriendRequest, FriendList
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from .models import  AcceptedRequest,Message,ChatRoom,Rating
from django.shortcuts import get_object_or_404
@login_required
def send_friend_request(request, receiver_id):
    if request.method == 'POST':
        sender = request.user
        receiver = CustomUser.objects.get(id=receiver_id)
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Check if a friend request already exists
        existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, source=source, destination=destination, date=date, time=time)
        if existing_request.exists():
            messages.warning(request, 'Friend request already sent.')
        else:
            friend_request = FriendRequest(sender=sender, receiver=receiver, source=source, destination=destination, date=date, time=time)
            friend_request.save()
            messages.success(request, 'Friend request sent successfully.')

    # Fetch friend requests where the receiver is the current user
    invitations = FriendRequest.objects.filter(receiver=request.user)

    # Fetch friend requests where the sender is the current user
    requests = FriendRequest.objects.filter(sender=request.user)

    context = {
        'invitations': invitations,
        'requests': requests,
    }

    return render(request, 'hackniterequests1.html', context)

@login_required
def accept_friend_request(request, request_id):
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id=request_id)
        friend_request.accept()
        messages.success(request, 'Friend request accepted successfully.')

    # Filter accepted requests where the current user is either the sender or receiver
    accepted_requests = AcceptedRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')  # Sort by timestamp in descending order

    context = {
        'accepted_requests': accepted_requests,
    }

    # Redirect to the desired URL
    return redirect('history')  # Replace 'hackniteridehistory' with your actual URL name

@login_required
def history(request):
    # Filter accepted requests where the current user is either the sender or receiver
    accepted_requests = AcceptedRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')  # Order by timestamp in descending order

    context = {
        'accepted_requests': accepted_requests,
    }

    return render(request, 'hackniteridehistory.html', context)


@login_required
def decline_friend_request(request, request_id):
    if request.method == 'POST':
        try:
            friend_request = FriendRequest.objects.get(id=request_id)
            friend_request.delete()
            messages.success(request, 'Friend request declined successfully.')
        except FriendRequest.DoesNotExist:
            messages.error(request, 'Friend request not found or you are not authorized to decline it.')
    return redirect('myrides')  # Redirect to the user's profile page or any desired page


@login_required
def cancel_friend_request(request, request_id):
    if request.method == 'POST':
        try:
            friend_request = FriendRequest.objects.get(id=request_id, sender=request.user)
            friend_request.delete()
            messages.success(request, 'Friend request canceled successfully.')
        except FriendRequest.DoesNotExist:
            messages.error(request, 'Friend request not found or you are not authorized to cancel it.')
    return redirect('myrides')  # Redirect to the user's profile page or any desired page

@login_required
def myrides(request):
    invitations = FriendRequest.objects.filter(receiver=request.user)

    # Fetch friend requests where the sender is the current user
    requests = FriendRequest.objects.filter(sender=request.user)

    context = {
        'invitations': invitations,
        'requests': requests,
    }

    return render(request,'hackniterequests1.html',context)

@login_required
def create_chat_room(request):
    if request.method == 'POST':
        # Get sender and receiver IDs from the form data
        sender_id = request.POST.get('sender_id')
        receiver_id = request.POST.get('receiver_id')
        
        # Fetch the sender and receiver objects from the database
        sender = CustomUser.objects.get(pk=sender_id)
        receiver = CustomUser.objects.get(pk=receiver_id)
        
        # Check if a chat room already exists between these users
        existing_room = ChatRoom.objects.filter(user1=sender, user2=receiver).first()
        if existing_room:
            return redirect(reverse('room', kwargs={'room_id': existing_room.id}))
        else:
            # Create a new chat room if one doesn't exist
            new_room = ChatRoom.objects.create(user1=sender, user2=receiver)
            return redirect(reverse('room', kwargs={'room_id': new_room.id}))
    else:
        return redirect('history')  # Redirect to home page if not a POST request
    

@login_required
def hacknite_chat_view(request, room_id):
    # Get the ChatRoom object or return a 404 error if not found
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Filter all message objects related to the given room and order by timestamp
    messages = Message.objects.filter(room=room).order_by('timestamp')
    
    # Pass the room and messages to the template context
    context = {
        'room': room,
        'messages': messages,
    }
    
    # Render the template with the provided context
    return render(request, 'hacknitechat.html', context)

@login_required
def hacknite_chat_send(request, room_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        print(content)
        room = get_object_or_404(ChatRoom, id=room_id)

        if request.user == room.user1:
            sender = room.user1
            receiver = room.user2
        else:
            sender = room.user2
            receiver = room.user1

        message = Message.objects.create(content=content, sender=sender, receiver=receiver, room=room)
        return redirect('room', room_id=room_id)
    else:
        return redirect('room', room_id=room_id)

@login_required
def rate_user(request, user_id):
    rated_user = get_object_or_404(CustomUser, pk=user_id)
    
    if request.method == 'POST':
        # Retrieve the rating value and feedback from the form
        rating_value = int(request.POST.get('rating'))
        feedback = request.POST.get('feedback')

        # Check if a rating already exists for the user
        rating, created = Rating.objects.get_or_create(rated_user=rated_user)

        # If a new rating is given, add it to the existing rating
        if created:
            rating.add_rating(rating_value)
            rating.save()
        else:
            # Update the rating if it already exists
            rating.add_rating(rating_value)
            rating.save()
        
        # Add feedback to the rating
        if feedback:
            rating.feedback = feedback
            rating.save()
        
        # Redirect to a success page or any desired page
        return redirect('history')  # Replace 'success_page' with your actual URL name

    else:
        # Render the rating form template
        return render(request, 'rating_form.html', {'user_id': user_id})
    
@login_required
def rate_page_view(request, user_id):
    # Retrieve the CustomUser object corresponding to the user_id
    rated_user = get_object_or_404(CustomUser, pk=user_id)
    context = {
        'rated_user': rated_user,
    }
    return render(request, 'hackniteratings.html', context)


