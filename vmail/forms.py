from django import forms


class Login(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class Message(forms.Form):
    sender = forms.EmailField(required=False)
    subject = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea)
    recipient = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)

