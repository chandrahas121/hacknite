
from django.urls import path,include
from drive_connect import views
urlpatterns = [
    path('',views.home,name="home"),
    path('profile',views.profile,name="profile"),
    path('search_users',views.search_users,name="search_users"),
    # path('/chat',include('chat.urls'))
]
