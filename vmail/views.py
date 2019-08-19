import smtplib
import ssl
import imaplib
import email
import imapclient
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import render
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
    return render(request, 'home_page.html')


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
            subject = form.cleaned_data['subject']
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = recipient
                part = MIMEText(message, 'plain')
                msg.attach(part)
                server = smtplib.SMTP_SSL(host, port)
                server.login(sender, password)
                mail = msg.as_string()
                server.sendmail(sender, recipient, mail)
                print(mail)
                return render(request, 'send_mail.html', {'success': "mail sent", 'form': message_form})
            except Exception as e:
                return render(request, 'send_mail.html', {'exception': "sorry, {}".format(e), 'form': message_form})
        else:
            return render(request, 'send_mail.html', {'invalid': 'invalid form', 'form': message_form})
    return render(request, 'send_mail.html.html', {"error": 'your request type is invalid', 'form': message_form})


def view_mail(request):
    server = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    imapClientServer = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    imapClientServer.login(request.session['email'], request.session['password'])
    server.login(request.session['email'], request.session['password'])
    server.select('"Inbox"')

    select_info = imapClientServer.select_folder('INBOX')
    messages = imapClientServer.search('ALL')

    count = select_info[b'EXISTS']

   # for msgid,data in imapClientServer.fetch(messages, ['ENVELOPE']).items: 
   #    message_id = msgid #message_id stores the message id of each mesasge in the loop


    typ1, message_numbers = server.search(None, 'ALL')  # change variable name, and use new name in for loop
    mail_messages = list()  # create  a list to hold mails
    email_subjects = list()  # create a list holding email subjects
    mail_senders = list()  # create a list holding email senders

    for num in message_numbers[0].split():
        typ, data = server.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        email_subject = msg['subject']
        email_from = msg['from']
        # print(msg['message-id'])
        print('From : ' + email_from + '\n')
        print("Subject:" + email_subject + "\n")

        if msg.is_multipart():
            for part in msg.walk():
                message = part.get_payload(decode=True)
                if msg['Subject'] and msg['From'] and message is not None:
                    mail_messages.append(
                        [message.decode('utf-8'), msg['message-id'], msg['Subject'], msg['From'][:-10], msg['date'][17:-12], num.decode()] )
                    print((mail_messages[0][3])[:-10])
        #  email_subjects.append(email_subject)
        #  mail_senders.append(email_from)

    return render(request, 'mails.html',
                  {'subject': email_subjects, 'sender': (mail_messages[0][3])[:-10], 'message': mail_messages,
                   'count': count})


def details(request, mid):
    server = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    server.login(request.session['email'], request.session['password'])
    server.select('"[Gmail]/All Mail"')
    message_details = list()
    typ, message_num = server.search(None, '(HEADER Message-ID "{}")'.format(
        mid))  # change variable name, and use new name in for loop
    for num in message_num:
        typ, data = server.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        subject = msg['subject']
        email_from = msg['from']
        time = msg['date']
        if msg.is_multipart():
            for part in msg.walk():
                msg_body = part.get_payload(decode=True)
                if msg_body is not None:
                    message_details.append([email_from, msg_body, subject, time])

    return render(request, 'inbox_details.html',
                  {'body': message_details[0][1].decode('utf-8'), 'subject': subject, 'from': email_from,
                   'time': time})


def delete_mail(request, mid):
    server = imapclient.IMAPClient('imap.gmail.com')
    server.login(request.session['email'], request.session['password'])
    server.select_folder('inbox')
    server.delete_messages(mid)
    return render(request, 'trash_success.html')


def log_out(request):
    form = Login()
    del request.session['email']
    return render(request, 'index.html', {'form': form})
