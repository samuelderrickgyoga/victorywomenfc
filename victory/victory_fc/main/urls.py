from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('players/', views.player_list, name='player_list'),
    path('players/<int:pk>/', views.player_detail, name='player_detail'),
    path('matches/', views.match_list, name='match_list'),
    path('matches/<int:pk>/', views.match_detail, name='match_detail'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('donate/', views.donation, name='donation'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('volunteer/success/', views.volunteer_success, name='volunteer_success'),
    path('contact/', views.contact, name='contact'),
    path('sponsor/', SponsorView.as_view(), name='sponsor'),
    path('coaches/', views.coaches_list, name='coaches_list'),
    path('coaches/<int:pk>/', views.coach_detail, name='coach_detail'),
    path('programs/', views.programs, name='programs'),
    path('success-stories/', success_stories, name='success_stories'),
    path('gallery/', views.gallery_list, name='gallery'),
    path('like/<int:pk>/', views.like_item, name='like_item'),
    path('add-reaction/', views.add_reaction, name='add_reaction'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
]
