from django import forms


class Login(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class Message(forms.Form):
    subject = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'id': 'message'}))
    recipient = forms.EmailField(required=False, widget=forms.TextInput(attrs={'id': 'recipient'}))
