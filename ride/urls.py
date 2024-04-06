from django.urls import path
from . import views

urlpatterns = [
    
    path('send_friend_request/<int:receiver_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('cancel_friend_request/<int:request_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('',views.myrides,name="myrides"),
    path('history',views.history,name="history"),
    path('chat/', views.create_chat_room, name='create_chat_room'),
    path('rate/<int:user_id>/', views.rate_page_view, name='rate_page_view'),
    path('rate/<int:user_id>/send', views.rate_user, name='rate_user_send'),
    # URL pattern for individual chat rooms using room IDs
    path('chat/room/<int:room_id>/', views.hacknite_chat_view, name='room'),
    path('chat/room/<int:room_id>/send/', views.hacknite_chat_send, name='hacknite_chat_send'),
]
