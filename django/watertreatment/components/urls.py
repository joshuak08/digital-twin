from django.urls import path
from . import views

# Map url to function in views module
urlpatterns = [
    path('', views.home, name="components-home"),
    path('types/', views.types, name="components-types"),
    path('types/<str:type>/', views.elementsOfType, name="components-elements-of-type"),
    path('types/<str:type>/<int:ID>/', views.elements, name="components-elements"),
    path('revit-model/', views.revitModel, name="components-revit-model"),
	path('simulation/', views.simulation, name="components-simulation"),
    path('carousel/', views.carousel, name="components-carousel")
]
