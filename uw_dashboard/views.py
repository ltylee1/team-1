from django.shortcuts import render
from django.views.generic import TemplateView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from uw_dashboard.forms import UploadFileForm
from uw_dashboard.models import Reporting_Service
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

reporting = Reporting_Service(None)

class Homepage(LoginRequiredMixin, TemplateView):
    template_name = "homepage.html"

class UploadView(LoginRequiredMixin, TemplateView):
    template_name = "upload.html"
    form_class = UploadFileForm

    def upload(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print "uploading file"
            myfile = form.cleaned_data['File_To_Upload']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            file_path = fs.path(uploaded_file_url)
            reporting.import_data(file_path, int(form.cleaned_data['Funding_Year']), form.cleaned_data['Overwrite_data'])
            return HttpResponseRedirect('homepage.html')

        else:
            return HttpResponseRedirect('homepage.html')

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request, *args, **kwargs):
        return self.upload(request)


class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        reporting = Reporting_Service(user)
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class MapView(LoginRequiredMixin, TemplateView):
    template_name = "map.html"

class AddUserView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "addUser.html"
    form_class = UserCreationForm
    model = User

    success_url = reverse_lazy("addUser")
    success_message = "%(username)s was created successfully"

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)

        for error in form.non_field_errors():
            messages.error(self.request, error)

        return super(AddUserView, self).form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_admin:
            messages.error(request, "Require administrator authentication to create new users")
            return self.handle_no_permission()

        return super(AddUserView, self).dispatch(request, *args, **kwargs)

class SearchResultsView(LoginRequiredMixin, TemplateView):
    template_name = "search-results.html"
