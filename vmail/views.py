import imaplib,smtplib, ssl
from django.shortcuts import render
from .forms import Login, Message

# Create your views here.
login_form = Login()
message_form = Message()
host = 'smtp.gmail.com'
port = 465
# create a secure context ssl
context = ssl.create_default_context()


def index(request):
    if request.method == 'POST':
        form = Login()
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                with smtplib.SMTP_SSL(host, port, context=context) as server:
                    server.login(email, password)
            except Exception as e:
                return render(request, 'index.html', {'exception': e})

    return render(request, 'index.html', {'form': login_form, })


def send_mail(request):
    sender = login_form.cleaned_data['email']
    password = login_form.cleaned_data['password']
    recipient = message_form.cleaned_data['recipient']
    message = message_form.cleaned_data['message']
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(host, port)
        server.starttls(context=context)  # Secure the connection
        server.login(sender, password)
        server.send_message(sender, recipient, message )
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
    return render(request, 'send_mail.html', {'login_form': login_form, 'message_form': message_form})


def view_mail(request):
    # connect to host using ssl
    imap = imaplib.IMAP4_SSL(host)

# login to server
    imap.login(login_form.cleaned_data['email'], login_form.cleaned_data['password'])

    imap.select('Inbox')
    tmp, data = imap.search(None, 'ALL')
    for num in data[0].split():
        tmp, data = imap.fetch(num, '(RFC822)')
        message = ('Message: {0}\n'.format(num))
        text = (data[0][1])
        break
    imap.close()
    return render(request, 'mails.html', {'message': message, 'text': text })


def delete_mail(request):
    pass


def home_page(request):
    return render(request, 'home_page.html')
