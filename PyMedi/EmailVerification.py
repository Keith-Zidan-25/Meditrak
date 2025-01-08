from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random

def generate_verification_code():
    code = random.randint(100000,999999)
    return code

def send_verification_email(email):
    
    verification_code = generate_verification_code()
    
    sender_email = '' #sender email or your email
    receiver_email = email
    subject = 'Email Verification'
    body = f'Your user verification code is: {verification_code}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, '' ) #enter email password
        server.send_message(msg)
        
    return verification_code

def send_appointment_notif(email,firstname,lastname,date,time):
    sender_email = '' #sender email or your email
    receiver_email = email
    subject = 'Email Verification'
    body = f'You have a appointment with: {firstname} {lastname} on {date} at {time}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, '') #enter email password
        server.send_message(msg)

