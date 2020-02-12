from django import forms

class FormQA(forms.Form):
    context = forms.CharField()
    question = forms.CharField()

