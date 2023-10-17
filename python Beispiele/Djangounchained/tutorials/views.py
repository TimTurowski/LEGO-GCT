from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Einzelteil
from .serializers import EinzelteilSerializer
from rest_framework.decorators import api_view
