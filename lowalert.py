import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, login, password):
    # Create a MIMEMultipart object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the body with the msg instance
    message.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(login, password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Your Gmail SMTP details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    receiver_email = "nevers.matthew@gmail.com"
    subject = "Test Email"
    body = "This is a test email sent using Python."
    
    # Gmail credentials
    login = "openwsalerts@gmail.com"
    password = "blqe wcmt ypga ebiy"  # For 2FA accounts, use an app password

    send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, login, password)
