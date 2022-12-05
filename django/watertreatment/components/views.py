from django.shortcuts import render
from .models import Post

"""
Works in a MVC Pattern 
Model - models.py
View - templates (.html)
Controller - views.py 
"""


def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'components/home.html', context)


def about(request):
    return render(request, 'components/about.html', {'title': 'About'})

def elements(request):
    types = {"pipe": 33, "sandfilter": 4, "electrics": 7}
    context = {'elements': "Wazaaa", 'title': "Elements", "types": types}

    return render(request, 'components/elements.html', context)

def elementsOfType(request, type):
    elements = {"pipe": ["12", "445", "354"], "sandfilter": ["55"], "electrics" : ["49"]}
    context = {"type": type, "elements": elements[type]}
    return render(request, 'components/elements-of-type.html', context)

def element(request, type, elementID):
    params = {"name": "default", "height": 12, "volume": 23}
    context = {"elementID": elementID, "params": params, "type": type}
    return render(request, 'components/element.html', context)

def revitModel(request):
    return render(request, 'components/revit-model.html')

