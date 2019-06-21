import smtplib
import ssl
import imaplib
import email
import string
from django.shortcuts import render
from .forms import Message, Login
from django.views.generic import View

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
    email = 'not logged in'
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            request.session['email'] = form.cleaned_data['email']
            request.session['password'] = form.cleaned_data['password']

            try:
                with smtplib.SMTP_SSL(host, port, context=context) as server:
                    server.login(email, password)
                    return render(request, 'home_page.html')
            except Exception as e:
                return render(request, 'index.html', {'exception': e, 'form': login_form})
        else:
                return render(request, 'index.html', {'invalid_form': 'Sorry, the form was invalid', 'form': login_form})
    return render(request, 'index.html', {"error": 'your request type is invalid', 'form': login_form, 'email': email})


def compose_view(request):
    return render(request, "send_mail.html", {'form': message_form})


def send_mail(request):
    if request.method == 'POST':
        form = Message(request.POST)
        print('entered first if')
        if form.is_valid():
            sender = request.session['email']
            password = request.session['password']
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
                        return render(request, 'send_mail.html', {'invalid': 'invalid form', 'form': message_form})
    return render(request, 'send_mail.html.html', {"error": 'your request type is invalid', 'form': message_form})


def view_mail(request):
    server = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    server.login(request.session['email'], request.session['password'])
    server.select()

    typ, message_numbers = server.search(None, 'ALL')  # change variable name, and use new name in for loop
    mail_messages = list()  # create  a list to hold mails
    email_subjects = list()  # create a list holding email subjects
    mail_senders = list()  # create a list holding email senders
    messageID = list()
    messageList = list()

    for num in message_numbers[0].split():
        typ, data = server.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
                # print(msg['message-id'])

                message = msg.get_payload(decode=True)

                print('From : ' + email_from + '\n')
                if email_subject is None:
                    pass
                else:
                    print("Subject:" + email_subject + "\n")
                # print(type(msg['message-id']))
                if message is not None:

                    mail_messages.append([message.decode('utf-8'), msg['message-id']])
                    email_subjects.append(email_subject)
                    mail_senders.append(email_from)

    return render(request, 'mails.html', {'subjects': email_subjects, 'senders': mail_senders, 'messages': mail_messages})  # {'message': message, 'text': text })


def details(request, mid):
    server = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    server.login('voiceemailproject@gmail.com', 'VoiceEmailProject')
    server.select()
    typ, message_num = server.search(None, '(HEADER Message-ID "{}")'.format(mid))  # change variable name, and use new name in for loop
    for num in message_num:
        typ, data = server.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        msg_body = msg.get_payload(decode=True)
        body = msg_body.decode('utf-8')
        subject = msg['subject']
        email_from = msg['from']
        time = msg['date']
    return render(request, 'inbox_details.html', {'body': body, 'subject': subject, 'from': email_from, 'time': time})


def delete_mail(request):
    return render(request, 'mails.html')


def log_out(request):
    form = Login()
    del request.session['email']
    return render(request, 'index.html', {'form': form})


def test(request):

    return render(request, 'test.html')


class Mail(View):
    pass