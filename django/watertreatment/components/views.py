# from curses.ascii import HT
from django.shortcuts import render

# Objects data we want to display
posts = [
    {
        'name': 'firstComponent',
        'source': 'pyRevit',
        'params':
            {
                'Width': 'w',
                'Height': 'h',
                'Length': 'l',
            },
        'content': 'first content',
    },
    {
        'name': 'secondComponent',
        'source': 'pyRevit',
        'params':
            {
                'Width': 1,
                'Height': 2,
                'Length': 3,
            },
        'content': 'first content',
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
