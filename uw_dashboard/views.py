from django.shortcuts import render
from django.views.generic import TemplateView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy

class Homepage(LoginRequiredMixin, TemplateView):
    template_name = "homepage.html"

class UploadView(LoginRequiredMixin, TemplateView):
    template_name = "upload.html"

class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class MapView(LoginRequiredMixin, TemplateView):
    template_name = "map.html"

class AddUserView(LoginRequiredMixin, TemplateView):
    template_name = "addUser.html"

class SearchResultsView(LoginRequiredMixin, TemplateView):
    template_name = "search-results.html"
