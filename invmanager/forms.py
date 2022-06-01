from django import forms


class AddEmployee(forms.Form):
    last_name = forms.CharField(label="Last Name", max_length=200)
    first_name = forms.CharField(label="First Name", max_length=200)
    email = forms.EmailField()
    #TODO Many to Many fields


class AddGadget(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    number = forms.IntegerField(label="Machinery Number")
    image = forms.ImageField(label="Image")
    installation_date = forms.DateField(label="Date of Installation")
    # TODO Many to Many fields


class AddAppointment(forms.Form):
    type = forms.ChoiceField(label="Type", choices=("Maintenance", "Inspection", "Replacement"))
    interval = forms.IntegerField(label="Interval")
    last_appointment = forms.DateField(label="Last Appointment")
    next_appointment = forms.DateField(label="Next Appointment")

    additional_information = forms.CharField(label="Additional Information", max_length=500)


class AddLocation(forms.Form):
    street = forms.CharField(label="Street", max_length=150)
    house_number = forms.CharField(label="House Number", max_length=50)
    postal_code = forms.CharField(label="Postal Code", max_length=50)
    city = forms.CharField(label="City", max_length=150)
    country = forms.CharField(label="Country", max_length=150)


class AddGadgetType(forms.Form):
    type = forms.CharField(label="GadgetType", max_length=50)
