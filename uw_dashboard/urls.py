from django.conf.urls import url, include

from .views import Homepage, UploadView, LoginView, AddUserView, MapView, LogoutView, SearchResultsView, SetPasswordView

urlpatterns = [
    url(r'^$', Homepage.as_view(), name='index'),
    url(r'^homepage.html$', Homepage.as_view(), name='homepage'),
    url(r'^upload.html$', UploadView.as_view(), name="upload"),
    url(r'^login.html$', LoginView.as_view(), name="login"),
    url(r'^logout.html$', LogoutView.as_view(), name="logout"),
    url(r'^addUser.html$', AddUserView.as_view(), name="addUser"),
    url(r'^map.html$', MapView.as_view(), name="map"),
    url(r'^searchResults.html$', SearchResultsView.as_view(), name='searchResults'),
    url(r'^resetPassword.html$', SetPasswordView.as_view(), name="resetPassword")
]
