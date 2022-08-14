import smtplib
from email.mime.text import MIMEText
import m_key


def send_mail(customer, email, cat, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = m_key.m_username
    password = m_key.m_pwd
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Email: {email}</li><li>Service: {cat} </li><li>Rating {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'vakahal90@gmail.com'
    receiver_email = 'akahal.info@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'SEO Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email


    # Send Email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())