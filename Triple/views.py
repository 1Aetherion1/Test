from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'Title':'Home',
        'Content': 'Главная страница магазина - HOME',
        'list': ['first','second'],
        'is_authenticated': False,
    }
    return  render(request,'Triple/index.html',context)

def about(request):
    return  HttpResponse("About page")
