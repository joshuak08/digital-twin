# from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Objects data we want to display
posts = [
    {
        'name': 'First Component',
        'content': 'First content',
        'params':
            {
                'Width': 'w',
                'Height': 'h',
                'Length': 'l',
            },
    },
    {
        'name': 'Second Component',
        'content': 'Second content',
        'params':
            {
                'Width': 1,
                'Height': 2,
                'Length': 3,
            },
    },
    {
        'name': 'Third Component',
        'content': 'Third content',
        'params':
            {
                'Width': 1,
                'Height': 2,
                'Length': 3,
            },
    },
    {
        'name': 'Fourth Component',
        'content': 'Fourth content',
        'params':
            {
                'Width': 1,
                'Height': 2,
                'Length': 3,
            },
    },
    {
        'name': 'Dummy  Component',
        'content': 'Baka content',
        'params':
            {
                'Width': 1,
                'Height': 2,
                'Length': 3,
            },
    },
    {
        'name': 'Dummy  Component',
        'content': 'Baka content',
        'params':
            {
                'Width': 1,
                'Height': 2,
                'Length': 3,
            },
    },

]


def home(request):
    # return HttpResponse('<h1>Water Treatment Components</h1>')
    context = {
        'posts': posts
    }
    return render(request, 'components/home.html', context)


def about(request):
    return render(request, 'components/about.html', {'title': 'about'})


def time(request):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    context = {
        'curr_time': now
    }
    return render(request, 'components/time.html', context)
