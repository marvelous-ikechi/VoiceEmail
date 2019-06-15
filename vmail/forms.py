from django import forms


class Login(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class Message(forms.Form):
    subject = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea)
    recipient = forms.EmailField(required=False)
