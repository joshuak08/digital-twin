from django.urls import path
from . import views

# Map url to function in views module
urlpatterns = [
    path('', views.home, name="components-home"),
    path('about/', views.about, name="components-about"),
    path('time/', views.time, name="components-time")
]
