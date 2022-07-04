from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.TestDetail.as_view()),
    path('map/', views.MapDetail.as_view())
]