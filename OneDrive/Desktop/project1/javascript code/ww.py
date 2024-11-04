import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
smtp_server='smtp.gmail.com'
smtp_port=587
smtp_user='msrikanth0503@gmail.com'
smtp_password='nawi euye hcdp glsn'
sender='msrikanth0503@gmail.com'
receiver='rogulsiva2002@gmail.com'
subject="blah blah"
body='sample message'
msg=MIMEMultipart()
msg['from']=sender
msg['To']=receiver
msg['subject']=subject
msg.attach(MIMEText(body,'plain'))
# try:
server=smtplib.SMTP(smtp_server,smtp_port)
server.starttls()
server.login(smtp_user,smtp_password)
server.sendmail(sender,receiver,msg.as_string())
print("Email sent successfully")
# except Exception as e:
#     print("failed to send mail")
# finally:
#     server.quit()