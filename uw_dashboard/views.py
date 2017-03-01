from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
from django.http import HttpResponse

class Homepage(TemplateView):

    def get_template_names(self):
        return "homepage.html"

