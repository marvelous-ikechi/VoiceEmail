

import imaplib, smtplib, ssl
from django.shortcuts import render, HttpResponseRedirect
from .forms import Message, Login


# Create your views here.
login_form = Login()
message_form = Message()
port = 465  # For SSL
host = 'smtp.gmail.com'
# create a secure context ssl
context = ssl.create_default_context()


def index(request):
    return render(request, 'index.html', {'form': login_form, })


def home_page(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                with smtplib.SMTP_SSL(host, port, context=context) as server:
                    server.login(email, password)
                    return render(request, 'home_page.html')
            except Exception as e:
                return render(request, 'index.html', {'exception': e, 'form': login_form})
    return render(request, 'index.html', {"error": 'your request type is invalid', 'form': login_form })


def compose_view(request):
    return render(request, "send_mail.html", {'form': message_form})


def send_mail(request):
    if request.method == 'POST':
        form = Message(request.POST)
        print('entered first if')
        if form.is_valid():
            sender = form.cleaned_data['sender']
            password = form.cleaned_data['password']
            message = form.cleaned_data['message']
            recipient = form.cleaned_data['recipient']
            try:
                with smtplib.SMTP_SSL(host, port, context=context) as server:
                    server.login(sender, password)
                    server.sendmail(sender, recipient, message)
                    print(sender,message,recipient,password)
                return render(request, 'send_mail.html', {'success':"mail sent", 'form':message_form})

            except:
                return render(request, 'send_mail.html', {'exception':"sorry, something isn't right!", 'form': message_form})
        else:
            print('out of second if')
            return render(request, 'send_mail.html', {'invalid': 'invalid form', 'form': message_form})
    print('outside if')
    return render(request, 'send_mail.html.html', {"error": 'your request type is invalid', 'form': message_form })


def view_mail(request):
    return render(request, 'mails.html')  # {'message': message, 'text': text })



def delete_mail(request):
    return render(request, 'mails.html')


def log_out(request):
    pass


def test(request):

    return render(request, 'test.html')


