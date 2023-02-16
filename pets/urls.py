from django.urls import path, re_path
from . import views

urlpatterns = [
    path("pets/", views.PetView.as_view()),
    path("pets/<int:pet_id>/", views.PetDetailView.as_view()),
]
