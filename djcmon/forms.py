from django import forms

class ManagerForm(forms.Form):
    email = forms.EmailField(label="Email")
