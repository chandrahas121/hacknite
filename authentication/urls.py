from django.contrib import admin
from django.urls import path,include

from authentication import views
from django_project.views import home_view
urlpatterns = [
  #path('',home_view),
  path('signup', views.signup, name="signup"),
  path('login', views.login, name="login"),
  path('logout',views.logout,name="logout"),
  #path('signout', views.signout, name="signout"),
]