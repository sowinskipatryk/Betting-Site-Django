from django.shortcuts import render, redirect
from .models import Team


def table(request):
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'table.html', context)


def matches(request):
    context = {}
    return render(request, 'matches.html', context)


def index(request):
    return redirect('/table')
