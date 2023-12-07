import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Retrieve environment variables
sender_email = os.environ.get("EMAIL_ADDRESS")
sender_password = os.environ.get("EMAIL_PASSWORD")

# Use the variables in your code
# print(f"Email: {sender_email}, Password: {sender_password}")


# Function to send emails
def send_email(sender_email, sender_password):
    conn = sqlite3.connect("secretsanta.db")
    cursor = conn.cursor()

    # Fetch participants with their assigned recipients
    cursor.execute(
        "SELECT name, email, (SELECT name FROM participants WHERE id = assigned_recipient) AS recipient_name FROM participants WHERE assigned_recipient != 0"
    )
    participants = cursor.fetchall()
    print(participants)

    # Email configuration (change as needed)
    smtp_server = os.environ.get("SMTP_SERVER")  # Set SMTP server address
    smtp_port = os.environ.get("SMTP_PORT")  # Set SMTP port
    sender_name = "Père Noël"  # Set sender's name
    subject = "Oh oh oh, c'est le Père Noël !!!"  # Set email subject

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send emails to participants

    for participant in participants:
        participant_name, participant_email, recipient_name = participant

        # Email content
        message = MIMEMultipart()
        message["From"] = f"{sender_name} <{sender_email}>"
        message["To"] = participant_email
        message["Subject"] = subject

        # Adjusted French message with proper encoding
        body = f"Hello {participant_name},\n\nVous êtes le Père Noël de {recipient_name}!\n\nJoyeux Noël !"
        message.attach(MIMEText(body, "plain", "utf-8"))  # Ensure correct encoding

        # Send email
        server.sendmail(sender_email, participant_email, message.as_string())
        print(f"Email sent to {participant_email}.")

    # Close connection to the SMTP server
    server.quit()

    conn.close()


# Call the function to send emails
send_email(sender_email, sender_password)
