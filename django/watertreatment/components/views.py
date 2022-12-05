from django.shortcuts import render
from .models import Post
import json
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
    elements = Post.objects.all() 
    types = {}

    for i in elements:
        if i.name not in types:
            types[i.name] = 1 
        else:
            types[i.name] = types[i.name] + 1
    
    context = {'types' : types, 'title' : "Types"}
    return render(request, 'components/types.html' , context)

def elementsOfType(request, type):
    elements = Post.objects.filter(name=type)
    ids = []
    for i in elements:
        ids.append(i.elementID)
    context = {'elements' : ids, 'title' : "Elements of type " + type, 'type': type}
    return render(request, 'components/elements-of-type.html', context)

def element(request, type, ID):
    element = Post.objects.get(elementID = ID)
    params = element.params
    context = {'elementID' : ID, "params" : params}
    return render(request, 'components/element.html', context)
