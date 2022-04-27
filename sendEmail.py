from email.mime.text import MIMEText
import smtplib

def sendEmail(email, height, averageHeight, count):
    from_email = "myemailaddress@gmail.com"
    from_password = "myemailpassword"
    to_email= email


    subject = "height data"
    message=" hey there, your height is <strong>%s</strong>. Average height is <strong>%s</strong> out of <strong>%s</strong> people" %(height, averageHeight, count)

    msg=MIMEText(message, 'html')
    msg['subject']= subject
    msg['To'] = to_email
    msg['From'] = from_email

    # turn of less secure application sign in inside your google account settings
    gmail=smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.startls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
