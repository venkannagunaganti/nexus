'''Import necessary modules:
MIMEMultipart and MIMEText from email.mime.multipart and email.mime.text respectively are used to create a multipart message for the email.
MIMEBase and encoders from email.mime.base and email are used to handle the attachments and encode them correctly.
os is used to perform file-related operations.'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# =====================================================================================================================
#   Function name:  send_email
#   Author: Sneha Dalvi
#   Description: Automatically send mails to multiple receivers with attachments
#   Input Parameters: sender_email, sender_password, receiver_emails, subject, body, attachment_paths
#   Output Parameters:  NONE
#  How to invoke ? : send_email(sender_email, sender_password, receiver_emails, subject, body, attachment_paths=None)
#   Date created: 02/08/2023
#   Date last modified & Changes done: 02/08/2023
# =====================================================================================================================


def send_email(sender_email, sender_password, receiver_emails, subject, body, smtp_server,smtp,attachment_paths=None):
    # Set up the SMTP server
    smtp_server = smtp_server
    # The port number
    smtp_port = smtp

    try:
        # Create a multipart message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ', '.join(receiver_emails)
        message['Subject'] = subject

        # Add body to the email
        message.attach(MIMEText(body, 'plain'))

        if attachment_paths:
            # Attach multiple files
            for attachment_path in attachment_paths:
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
                message.attach(part)

        # Log in to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_emails, message.as_string())

        print("Email sent successfully!")



    except Exception as e:
        print("Error sending email:", str(e))



