from django.urls import path
from . import views
# from .views import line_chart, line_chart_json

# Map url to function in views module
urlpatterns = [
    path('', views.home, name="components-home"),
    path('types/', views.elements, name="components-types"),
    path('types/<str:type>/', views.elementsOfType, name="components-elements-of-type"),
    path('types/<str:type>/<int:ID>/', views.element, name="components-elements-of-type"),
    path('revit-model/', views.revitModel, name="components-revit-model"),
	path('simulation/', views.simulation, name="components-simulation"),
    path('carousel/', views.carousel, name="components-carousel"),
    path('test-form/', views.form, name="components-test-form"),
    path('graph/', views.graph, name="components-graph"),
]
