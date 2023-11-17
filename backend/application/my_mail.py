from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


def send_mail(to, subject, body, sub_type):
    host = 'localhost'
    port = 1025
    sender_email = 'harshilpandey03@gmail.com'
    sender_password = '1234'
    mail=MIMEMultipart()
    mail['To']=to
    mail['From']=sender_email
    mail['Subject']=subject
    mail.attach(MIMEText(body, sub_type))
    server=SMTP(host=host, port=port)
    server.login(user=sender_email, password=sender_password)
    server.send_message(mail)
    server.quit()

