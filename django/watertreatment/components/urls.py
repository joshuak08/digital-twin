from django.urls import path
from . import views

# Map url to function in views module
urlpatterns = [
    path('', views.home, name="components-home"),
    path('about/', views.about, name="components-about"),
    path('types/', views.elements, name="components-types"),
    path('types/<str:type>/', views.elementsOfType, name="components-elements-of-type"),
    path('types/<str:type>/<int:ID>/', views.element, name="components-elements-of-type")
]
