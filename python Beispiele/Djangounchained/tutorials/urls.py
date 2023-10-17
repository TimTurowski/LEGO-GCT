from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("api/tutorials", views.tutorial_list),
    re_path(r"^api/tutorials/(?P<pk>[0-9]+)$", views.tutorial_detail),
    path("api/tutorials/published", views.tutorial_list_published)
]
