from django import forms


class GuestLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField()


class RegisterMacForm(forms.Form):

    mac_address = forms.CharField()
