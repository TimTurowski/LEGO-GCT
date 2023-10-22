from django.urls import path
from . import views

urlpatterns = [
    path('eingabe/', views.eingabe),
]
