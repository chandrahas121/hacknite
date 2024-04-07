from django.db import models
from django.conf import settings
from drive_connect.models import UserTrip  # Import UserTrip from the correct module
from django.utils import timezone
class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        self.remove_friend(removee)
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        return friend in self.friends.all()


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_requests")
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=100, default='india')
    destination = models.CharField(max_length=100, default='Default Destination')
    date = models.DateField(default=timezone.now) 
    time = models.TimeField(default='12:00') 

    def __str__(self):
        return f"Friend request from {self.sender} to {self.receiver}"

    def accept(self):
        #sender_friend_list = FriendList.objects.get(user=self.sender)
        #receiver_friend_list = FriendList.objects.get(user=self.receiver)

        #if sender_friend_list and receiver_friend_list:
        #    sender_friend_list.add_friend(self.receiver)
        #    receiver_friend_list.add_friend(self.sender)
            AcceptedRequest.objects.create(
                sender=self.sender,
                receiver=self.receiver,
                source=self.source,
                destination=self.destination,
                date=self.date,
                time=self.time
            )
            self.delete()  # Delete the FriendRequest object
            self.is_active = False
            #self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()

class AcceptedRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accepted_sent_requests")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accepted_received_requests")
    source = models.CharField(max_length=100, default='india')
    destination = models.CharField(max_length=100, default='Default Destination')
    date = models.DateField(default=timezone.now) 
    time = models.TimeField(default='12:00') 
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Accepted request from {self.sender} to {self.receiver}"

class ChatRoom(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat room between {self.user1.username} and {self.user2.username}"
class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', default=1)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content}"

from django.db import models
from django.conf import settings
from django.utils import timezone

class Rating(models.Model):
    rated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings_received")
    average_rating = models.FloatField(default=0) # Total sum of ratings given by users
    num_ratings = models.IntegerField(default=0)  # Total number of users who rated
    feedback = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rating for {self.rated_user.username}"

    def add_rating(self, rating_value):
        # Update total rating and increment number of ratings
        
        if(self.num_ratings>0):
            self.average_rating=(((self.average_rating)*(self.num_ratings))+(rating_value))/(self.num_ratings+1)
        
        else:
            self.average_rating=rating_value
        self.num_ratings+=1
        self.save()
        user = self.rated_user
        user.rating=self.average_rating
        user.save()