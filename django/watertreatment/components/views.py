import os

from django.shortcuts import render
from .models import *
from .forms import *
from django.core import serializers
import json
from django.http import HttpResponseRedirect
import sys
sys.path.append("../../simulation-system")
import HelperFunctions

"""
Works in a MVC Pattern 
Model - models.py
View - templates (.html)
Controller - views.py 
"""


def home(request):
    context = {}
    return render(request, 'components/home.html', context)


def types(request):
    elements = Document.objects.all()
    types = {}

    for i in elements:
        if i.name not in types:
            types[i.name] = 1
        else:
            types[i.name] = types[i.name] + 1

    context = {'types': types, 'title': "Types"}
    return render(request, 'components/types.html', context)


def elementsOfType(request, type):
    elements = Document.objects.filter(name=type)
    ids = [i.elemID for i in elements]
    context = {'elements': ids, 'title': "Elements of type " + type, 'type': type}
    return render(request, 'components/elements-of-type.html', context)


def elements(request, type, ID):
    element = Document.objects.get(elemID=ID)
    params = json.loads(element.params)
    context = {'elementID': ID, "params": params, 'type': type}
    return render(request, 'components/element.html', context)


def revitModel(request):
    return render(request, 'components/revit-model.html', {'title': "Revit Model"})


def simulation(request):
    all_SimData = serializers.serialize("json",
                                        SimDataTable.objects.all())  # converts QuerySet into data types understandable by javascript
    return render(request, 'components/simulation.html', {'title': "Simulation", 'all_SimData': all_SimData})


def carousel(request):
    return render(request, 'components/carousel.html', {'title': "Carousel"})

def form(request):
    if request.POST:
        form = SimInputForm(request.POST)
        data = form.__dict__['data'].dict()
        if form.is_valid():
            data, initial_particulate = formDataManipulation(data)
            # HelperFunctions.basic_simulation(float(data['average_flow']), int(data['average_tss']), int(data['sim_length']), data['testing'])
            HelperFunctions.initial_particulate_simulation(float(data['average_flow']), float(data['average_tss']), int(data['sim_length']), initial_particulate, data['testing'])
            # redirected to simulation page to run immediately with new table name and id
            return HttpResponseRedirect('/simulation/')
    return render(request, 'components/input-form.html', {'title': "Form Testing", 'form': SimInputForm})


def formDataManipulation(data):
    if 'csrfmiddlewaretoken' in data:
        del data['csrfmiddlewaretoken']
    if 'testing' not in data:
        data['testing'] = False
    else:
        data['testing'] = True
    initial_particulate = [0 if data['tank0'] == '' else float(data['tank0']), 
                           0 if data['tank1'] == '' else float(data['tank1']), 
                           0 if data['tank2'] == '' else float(data['tank2']), 
                           0 if data['tank3'] == '' else float(data['tank3'])]
    return data, initial_particulate

def graph(request):
    all_SimData = serializers.serialize("json", SimDataTable.objects.all())  # converts QuerySet into data types understandable by javascript
    return render(request, 'components/graph.html', {'title': "Graph", 'all_SimData': all_SimData})
