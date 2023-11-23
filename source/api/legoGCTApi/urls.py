from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('eingabe/', views.eingabe),
    path('auth/', obtain_auth_token),
    path('verlauf/', views.verlauf),
    path('delete/', views.delete_set_entry)
]
