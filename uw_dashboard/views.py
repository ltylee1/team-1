from django.shortcuts import redirect
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
from django.views.generic.edit import CreateView, UpdateView
from uw_dashboard.forms import UploadFileForm, SetUserPasswordForm
from uw_dashboard.models import Reporting_Service
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import json

reporting = Reporting_Service(None)


class Homepage(LoginRequiredMixin, TemplateView):
    template_name = "homepage.html"


class UploadView(LoginRequiredMixin, TemplateView):
    template_name = "upload.html"
    form_class = UploadFileForm

    def upload(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = form.cleaned_data['File_To_Upload']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            file_path = fs.path(uploaded_file_url)
            try:
                result = reporting.import_data(str(file_path), int(form.cleaned_data['Funding_Year']),
                                  form.cleaned_data['Overwrite_data'], form.cleaned_data['File_type'])
            except:
                messages.error(request, "Error in parsing. Please upload a valid .csv file")
                return redirect(reverse_lazy('upload'))
            if not result:
                messages.error(request, "Please upload a .csv file")
                return redirect(reverse_lazy('upload'))
            else:
                fs.delete(filename)
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
            return redirect(reverse_lazy('homepage'))

        return super(AddUserView, self).dispatch(request, *args, **kwargs)


class SearchResultsView(LoginRequiredMixin, TemplateView):
    template_name = "search-results.html"

    def post(self, request, *args, **kwargs):
        context = reporting.query_data(request.POST)

        if context.get('results') == []:
            messages.error(request, "No data for selected filters")
            return redirect(reverse_lazy('search-page'))

        context["data_table"] = self.getDataTable(context["results"])
        return render(request, 'search-results.html', context)

    def getDataTable(self, results):
        keys = [
            "funding_stream",
            "donor_engagement",
            "year",
            "program_planner",
            "element_name",
            "city",
            "specific_element",
            "strategic_outcome",
            "city_grouping",
            "level_name",
            "target_population",
            "focus_area",
            "program_name"
        ]

        dataTable = [["Allocation",
                      "Funding Stream",
                      "Donor Engagement",
                      "Year",
                      "Program Planner",
                      "Element Name",
                      "City",
                      "Specific Element",
                      "Strategic Outcome",
                      "City Grouping",
                      "Level Name",
                      "Target Population",
                      "Focus Area",
                      "Program Name"]]

        for data in results:
            array = [data["allocation"]]
            array += [str(data[key]) for key in keys]
            dataTable.append(array)

        return json.dumps(dataTable)


class SearchPage(LoginRequiredMixin, TemplateView):
    template_name = "search-page.html"


class SetPasswordView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "resetPassword.html"
    form_class = SetUserPasswordForm

    success_url = reverse_lazy("homepage")
    success_message = "You have reset password for %(username)s successfully"

    def form_valid(self, form):
        try:
            user = User.objects.get(username=form.cleaned_data.get('username'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'User with the username does not exist')
            return redirect(reverse_lazy('resetPassword'))

        user.set_password(form.clean_new_password2())
        user.save()
        return super(SetPasswordView, self).form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)

        for error in form.non_field_errors():
            messages.error(self.request, error)

        return super(SetPasswordView, self).form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_admin:
            messages.error(request, "Require administrator authentication to reset passwords")
            return redirect(reverse_lazy('homepage'))

        return super(SetPasswordView, self).dispatch(request, *args, **kwargs)
