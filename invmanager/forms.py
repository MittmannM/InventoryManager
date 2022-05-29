from django import forms


class AddEmployee(forms.Form):
    last_name = forms.CharField(label="Last Name", max_length=200)
    first_name = forms.CharField(label="First Name", max_length=200)
    email = forms.EmailField()
