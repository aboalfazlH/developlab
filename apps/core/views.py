from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render

class MainPageView(TemplateView):
    template_name = "index.html"