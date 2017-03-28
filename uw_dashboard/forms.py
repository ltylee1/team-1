from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
import unicodedata

YEARS = (
    (2015, '2015/2016'),
    (2016, '2016/2017'),
    (2017, '2017/2018'),
)

TYPE = [
    ('output', 'Inventory and Outputs'),
    ('postal', 'Program Locations'),
]

# widget=forms.TextInput(attrs={'class': 'col-md-4'})
class UploadFileForm(forms.Form):
    File_To_Upload = forms.FileField(widget=forms.ClearableFileInput(attrs= {'class': 'upload_btn'}))
    Overwrite_data = forms.BooleanField(required=False)
    File_type = forms.ChoiceField(TYPE)
    Funding_Year = forms.ChoiceField(YEARS)

class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))

class SetUserPasswordForm(SetPasswordForm):
    username = forms.ModelChoiceField(queryset= User.objects.all().order_by('username'), to_field_name="username")

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self , *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2)
        return password2

class DeleteUserForm(forms.Form):
    username = forms.ModelChoiceField(queryset= User.objects.filter(profile__is_admin = False).order_by('username'), to_field_name="username")
