from django import forms

class GenerateForm(forms.Form):
    # costom = forms.CharField(  label = "Prefered text", required = False ,widget= forms.TextInput(attrs={'class':'form-control'}))
    rows = forms.IntegerField (label = "Number of Rows")
    col =   forms.IntegerField (label = "Number of Columns")
    time = forms.FloatField(label = "Time to generate in minutes")
    