from django import forms

class AreaForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    address = forms.CharField(label='Address', widget=forms.Textarea)
    mobile = forms.CharField(label='Mobile Number', max_length=10)
    age = forms.IntegerField(label='Age', min_value=1)
    area_sqft = forms.FloatField(label='Enter Area in Sq. Ft.', min_value=100)
