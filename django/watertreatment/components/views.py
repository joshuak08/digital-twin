# from curses.ascii import HT
from django.shortcuts import render

posts = [
    {
        'name': 'firstComponent',
        'source': 'pyRevit',
        'width': 'w',
        'height': 'h',
        'length': 'l',
        'content': 'first content',
    },
    {
        'name': 'secondComponent',
        'source': 'pyRevit',
        'width': '3',
        'height': '4',
        'length': '8',
        'content': 'second content',
    },
    {
        'name': 'thirdComponent',
        'source': 'pyRevit',
        'width': '3',
        'height': '4',
        'length': '8',
        'content': 'third content',
    },
    {
        'name': 'foruthComponent',
        'source': 'pyRevit',
        'width': '3',
        'height': '4',
        'length': '8',
        'content': 'fourth content',
    }
]


def home(request):
    # return HttpResponse('<h1>Water Treatment Components</h1>')
    context = {
        'posts': posts
    }
    return render(request, 'components/home.html', context)


def about(request):
    return render(request, 'components/about.html', {'title': 'about'})
