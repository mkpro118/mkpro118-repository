import smtplib
from email.message import EmailMessage
import os


Email_Password = os.environ.get('Django_Project_Email_Password')
Email_Address = os.environ.get('Django_Project_Email')

msg = EmailMessage()
msg['From'] = Email_Address
msg['To'] = 'mkpro118@gmail.com'
msg.set_content('Hi how are you?')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login(Email_Address, Email_Password)
    s.send_message(msg)
print('done')
