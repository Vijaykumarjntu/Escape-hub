from django.urls import path
from . import views

urlpatterns = [
    # Landing page
    path('', views.anonymous_login, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Matching
    path('start/', views.start_match, name='start_match'),
    path('check_match/', views.check_match, name='check_match'),
    
    # Room
    path('room/<str:room_id>/', views.room_view, name='room'),
    
    # Leave/exit
    path('leave/<str:room_id>/', views.leave_room, name='leave_room'),
    
    # WebSocket endpoint (for Django Channels)
    path('ws/chat/<str:room_id>/', views.websocket_endpoint, name='websocket'),

    path('profile/', views.profile_view, name='profile'),

    path('public-pages/', views.public_pages, name='public_pages'),
]
