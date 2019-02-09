from django import forms

class CountryForm(forms.Form):
   country = forms.CharField(required = True, widget=forms.TextInput(attrs={'class': "form-control"}),)
   year = forms.ChoiceField(choices=[(x, x) for x in range(1961, 2019)], widget=forms.Select(attrs={'class':'form-control'}))
   per_capita = forms.BooleanField(required = False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))

class CompareCountry(forms.Form):
   country_one = forms.CharField(required = True, widget=forms.TextInput(attrs={'class': "form-control"}))
   country_two = forms.ChoiceField(choices=[('United Kingdom', 'United Kingdom'), ('France', 'France'),
   ('Germany', 'Germany'), ('China', 'China'), ('Russia','Russia'), ('United States','United States'), ('Japan','Japan')], widget=forms.Select(attrs={'class':'form-control'}))