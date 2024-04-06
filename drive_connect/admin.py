from django.contrib import admin
from .models import UserTrip

class UserTripAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'destination', 'date', 'time')
    list_filter = ('source', 'destination', 'date')
    search_fields = ('source', 'destination', 'user__username')  # Allows searching by source, destination, and user's username

admin.site.register(UserTrip, UserTripAdmin)
