from django.shortcuts import render
from django.views.generic import TemplateView

class Homepage(TemplateView):
    template_name = "homepage.html"

class UploadView(TemplateView):
    template_name = "upload.html"

class LoginView(TemplateView):
    template_name = "login.html"

class MapView(TemplateView):
    template_name = "map.html"

class AddUserView(TemplateView):
    template_name = "addUser.html"