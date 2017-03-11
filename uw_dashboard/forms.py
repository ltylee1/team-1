from django import forms

YEARS = (
    (2016, '2015/2016'),
    (2017, '2016/2017'),
    (2018, '2017/2018'),
)

TYPE = (
    ('output', 'Inventory and Outputs'),
    ('postal', 'Program Locations'),
)

# widget=forms.TextInput(attrs={'class': 'text-center filter-text'})
class UploadFileForm(forms.Form):
    File_To_Upload = forms.FileField()
    Overwrite_data = forms.BooleanField(required=False)
    Funding_Year = forms.ChoiceField(YEARS)
    File_type = forms.ChoiceField(TYPE)
