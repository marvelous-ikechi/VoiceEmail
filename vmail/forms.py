from django import forms


class Login(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class Message(forms.Form):
    # sender's address will be imported from the Login form
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    recipient = forms.EmailField(required=True)

