from django import forms

class NextPageForm(forms.Form):
	token = forms.CharField(widget=forms.HiddenInput())