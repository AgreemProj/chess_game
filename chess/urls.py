from django.urls import path

from . import views
from .views import Pieces

urlpatterns = [
    path("<slug:slug>/", Pieces.as_view()),
]