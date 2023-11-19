from django.urls import path
from .views import search_logs

urlpatterns = [
    path('search/', search_logs, name='search_logs'),
]
