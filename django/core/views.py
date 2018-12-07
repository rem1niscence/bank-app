from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    template_name = 'index.html'
