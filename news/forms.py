from django import forms

class CommentForm(forms.Form):
    
    comment = forms.CharField( required = True ,widget= forms.Textarea(attrs={'class':'form-control'}))

class ReplyForm(forms.Form):
    reply = forms.CharField(required= True,widget = forms.TextInput(attrs={'class':'form-control'}))