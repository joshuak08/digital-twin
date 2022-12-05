from django.urls import path
from . import views

# Map url to function in views module
urlpatterns = [
    path('', views.home, name="components-home"),
    path('about/', views.about, name="components-about"),
    path('elements/', views.elements, name="components-elements"),
    path('elements/<str:type>/', views.elementsOfType, name="components-elements-of-type"),
    path('elements/<str:type>/<str:elementID>/', views.element, name="component-element"),
    path('revit-model/', views.revitModel, name="components-revit-model")
]
