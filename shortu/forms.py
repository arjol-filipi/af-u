from django import forms


class UrlForm(forms.Form):
    url = forms.URLField( label = "Your long url",widget= forms.URLInput(attrs={'class':'form-control'}))
    #CharField( label = "Your long url")
    costom = forms.CharField(  label = "Prefered text", required = False ,widget= forms.TextInput(attrs={'class':'form-control'}))
