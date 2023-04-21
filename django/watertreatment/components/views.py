import os

from django.shortcuts import render
from .models import Document, SimDataTable
from django.core import serializers
import json
from .forms import SimInputForm
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


def about(request):
    return render(request, 'components/about.html', {'title': 'About'})


def elements(request):
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
    ids = []
    for i in elements:
        ids.append(i.elemID)
    context = {'elements': ids, 'title': "Elements of type " + type, 'type': type}
    return render(request, 'components/elements-of-type.html', context)


def element(request, type, ID):
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
            del data['csrfmiddlewaretoken']
            if 'testing' not in data:
                data['testing'] = False
            else:
                data['testing'] = True
            print('From views.py current directory: ' + os.getcwd())
            HelperFunctions.basic_simulation(float(data['average_flow']), int(data['average_tss']), int(data['sim_length']), data['testing'])
            # HelperFunctions.initial_particulate_simulation(int(data['average_flow']), int(data['average_tss']), int(data['sim_length']), int(data['initial_particulates']), data['testing'])
        # redirected to simulation page to run immediately with new table name and id
        return HttpResponseRedirect('/simulation')
    # else:
    #     form = SimInputForm
    #     if 'submitted' in request.GET:
    #         submitted = True
    #
    return render(request, 'components/test-form.html', {'title': "Form Testing", 'form': SimInputForm})
