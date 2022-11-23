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
