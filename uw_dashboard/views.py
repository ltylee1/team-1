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
from uw_dashboard.forms import UploadFileForm, SetUserPasswordForm, DeleteUserForm
from uw_dashboard.models import Reporting_Service
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, models
import json, models

reporting = Reporting_Service(None)

class Homepage(LoginRequiredMixin, TemplateView):
    template_name = "homepage.html"

class Profile(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"


    def post(self, request, *args, **kwargs):
        query = "SELECT * FROM uw_dashboard_search_history"
        results = self.my_custom_sql(query)
        context= {}
        context["results"] = results
        return render(request, 'profile.html', context)

    def dictfetchall(self, cursor):
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
             results.append(dict(zip(columns, row)))
        return results    

    def my_custom_sql(self,query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = self.dictfetchall(cursor)
        return results




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
                                  form.cleaned_data['Overwrite_data'], str(form.cleaned_data['File_type']))
            except Exception as e:
                # messages.error(request, "Error in parsing. Please upload a valid .csv file")
                messages.error(request, "Error in parsing. Please upload a valid .csv file. Error message: %s" %(str(e)))
                fs.delete(filename)
                return redirect(reverse_lazy('upload'))
            if not result:
                messages.error(request, "Please upload a .csv file")
                fs.delete(filename)
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

    def get(self, request, *args, **kwargs):
        location_list = reporting.queryMap()
        return render(request, 'map.html', {'data_table': location_list})


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

        print context.get("results")[0]
        self.addFiltersToDatabase(context["filters"])
        context["data_table"] = self.getDataTable(context["results"])
        context["pie_table"] = self.getPieTable(context["results"])
        context["totals_table"] = self.getTotalsTable(context["totals"])
        context["filters_table"] = self.getFiltersTable(context["filters"])
        return render(request, 'search-results.html', context)

    def getDataTable(self, results):
        keys = [
            "program_name",
            "agency_name",
            "allocation",
            "funding_stream",
            "grant_start_date",
            "grant_end_date",
            "element_names",
            "program_description"
        ]

        dataTable = []

        for data in results:
            array = [str(data[key]) for key in keys]
            dataTable.append(array)

        return dataTable

    def getPieTable(self, results):
        keys = [
             "city",
        ]

        dataTable = [[
            "Allocation",
            "City"
        ]]

        for data in results:
            array = [data["allocation"]]
            array += [str(data[key]) for key in keys]
            dataTable.append(array)

        return json.dumps(dataTable)

    def getTotalsTable(self, results):
        keyNames = ["Seniors",
                      "Early Years",
                      "Counselling Sessions",
                      "Families",
                      "Programs",
                      "Mentors/Tutors",
                      "Workshops",
                      "Middle Years",
                      "Agencies",
                      "Meals/Snacks",
                      "Money Invested",
                      "Parent/Caregivers",
                      "Volunteers"]

        data = results[0]
        i =0
        for key in data:
            data[key] = [keyNames[i], str(data[key])]
            i = i + 1


        results[0] = data

        return results

    def getFiltersTable(self, results):
        keyNames = {"funding_year" : "Funding Year",
                    "focus_area" : "Focus Area",
                    "target_population" : "Target Population",
                    "program_elements" : "Program Elements",
                    "city" : "City Grouping",
                    "gfa" : "Geogrphic Focus Area",
                    "donor" : "Donor Engagement",
                    "money_invested" : "Money Invested"
                    }

        del results["Submit"]
        del results["csrfmiddlewaretoken"]

        # for key in results:
        #     results[key] = {keyNames[key]: str(results[key])}

        for key in results:
            results[key] = {keyNames[key] :  results[key]}
            filterList = results[key][keyNames[key]]
            filterMapKey = keyNames[key]
            j = 0
            for option in filterList:
                filterList[j] = str(option)
                j = j + 1
            results[key][keyNames[key]] = filterList

        return results

    def addFiltersToDatabase(self, results):
        funding_year=""
        focus_area=""
        target_population=""
        program_elements=""
        city=""
        gfa=""
        donor=""
        money_invested=""
        if "funding_year" in results:
            funding_year = results["funding_year"]
        if "focus_area" in results:
            focus_area = results["focus_area"]
        if "target_population" in results:
            target_population = results["target_population"]
        if "program_elements" in results:
            program_elements = results["program_elements"]
        if "city" in results:
            city = results["city"]
        if "gfa" in results:
            gfa = results["gfa"]
        if "donor" in results:
            donor = results["donor"]
        if "money_invested" in results:
            money_invested = results["money_invested"]

        search = models.Search_History( funding_year=funding_year,
                                        focus_area=focus_area,
                                        target_population=target_population,
                                        program_elements=program_elements,
                                        city_groupings=city,
                                        geographic_focus_area=gfa,
                                        donor_engagement=donor,
                                        money_invested=money_invested)
        search.save()

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

class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "deleteUser.html"
    form_class = DeleteUserForm

    success_url = reverse_lazy("homepage")
    success_message = "You have deleted %(username)s successfully"

    def form_valid(self, form):
        try:
            user = User.objects.get(username=form.cleaned_data.get('username'))
        except ObjectDoesNotExist:
            messages.error(self.request, 'User with the username does not exist')
            return redirect(reverse_lazy('deleteUser'))

        user.delete()
        return super(DeleteUserView, self).form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)

        for error in form.non_field_errors():
            messages.error(self.request, error)

        return super(DeleteUserView, self).form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_admin:
            messages.error(request, "Require administrator authentication to reset passwords")
            return redirect(reverse_lazy('homepage'))

        return super(DeleteUserView, self).dispatch(request, *args, **kwargs)

