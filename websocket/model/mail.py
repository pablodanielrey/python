import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class Mail:

    smtp_host = '163.10.17.115'
    smtp_user = 'campus'
    smtp_pass = 'supmac'

    def createMail(self,From,To,subject):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject,'utf-8')
        msg['From'] = From
        msg['To'] = To
        return msg

    def getHtmlPart(self,body):
        msg = MIMEText(body.encode('utf-8'),'html','utf-8')
        return msg

    def getTextPart(self,body):
        msg = MIMEText(body.encode('utf-8'),'plain','utf-8')
        return msg


    def sendMail(self, ffrom, tos, body):
      try:
          s = smtplib.SMTP(self.smtp_host)
          s.login(self.smtp_user,self.smtp_pass)
          s.sendmail(ffrom, tos, body)

      finally:
          s.quit()
