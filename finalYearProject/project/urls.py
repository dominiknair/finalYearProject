from django.urls import path
from .views import PreferencesCreateView, EventDetailView, interestedDetailView
from . import views

urlpatterns = [
    path('', views.home, name='project-home'),
    path('preferences/new/', PreferencesCreateView.as_view(), name='preferences-create'),
    path('preference1/', views.preference1, name='preference1'),
    path('about/', views.about, name='project-about'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('interested/<int:pk>/', interestedDetailView.as_view(), name='interested-detail'),
    path('addInterested/', views.addInterested, name='addInterested'),
    path('deleteInterested/', views.deleteInterested, name='deleteInterested'),
    path('interestedEvents/', views.interestedEvents, name='interestedEvents'),
    path('addToUserProfile/', views.addToUserProfile, name='addToUserProfile'),
    path('searchEvent/', views.searchEvent, name='searchEvent'),
    path('searchview1/', views.searchview1, name='searchview1'),
]
