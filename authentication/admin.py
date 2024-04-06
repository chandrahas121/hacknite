
# Register your models here.
# in admin.py
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'age')  # Add 'age' here if you want it to be displayed

admin.site.register(CustomUser, CustomUserAdmin)
