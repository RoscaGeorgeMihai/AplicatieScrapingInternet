import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self):
        self.smtpServer = 'smtp.gmail.com'
        self.smtpPort = 587
        self.smtpUser = '<INSERT YOUR SENDING MAIL HERE>'
        self.smtpPassword = '<INSERT YOUR MAIL PASSWORD CODE HERE>'

    def sendMail(self, toEmail, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.smtpUser
        msg['To'] = self.smtpPassword
        msg['Subject'] = subject
    
        body = body
        msg.attach(MIMEText(body, 'plain'))
    
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.smtpUser, self.smtpPassword)
                server.sendmail(self.smtpUser, toEmail, msg.as_string())
            print('Email sent successfully!')
    
        except Exception as e:
            print(f'Error while trying to send the email: {e}')