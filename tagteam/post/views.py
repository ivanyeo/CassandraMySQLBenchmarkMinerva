from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    return render(request, 'post/index.html', context)

from django.http import HttpResponse

def hello(request):
    return HttpResponse('hello world from Monica!')
