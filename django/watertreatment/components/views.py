# from curses.ascii import HT
from django.shortcuts import render

posts = [
	{ 
		'name' : 'firstComponent',
		'source' : 'pyRevit',
		'width' : 'w',
		'height' : 'h',
		'length' : 'l',
		'content' : 'first content',
		'codenum' : '#1'
	 },
	 { 
		'name' : 'secondComponent',
	 	'source' : 'pyRevit',
		'width' : '3',
		'height' : '4',
		'length' : '8',
		'content' : 'second content',
		'codenum' : '#2'
	 }
]

def home(request):
    # return HttpResponse('<h1>Water Treatment Components</h1>')
	context = {
		'posts' : posts
	}
	return render(request, 'components/home.html', context)

def about(request):
    return render(request, 'components/about.html', {'title' : 'about'})