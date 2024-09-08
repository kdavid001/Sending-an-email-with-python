import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Email details
smtp_server = "smtp.gmail.com"
port = 587
receiver_email = "RECIEVERS-EMAIL"

sender_email = "SENDERS-EMAIL"
password = 'PASSWORD'

# Email content
subject = "Test Email"
body = "This is a test email."

# Create the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))


#To Check for errors.
max_retries = 5  # Maximum number of retries
retry_delay = 60  # Delay between retries in seconds

server = None  # Initialize the server variable

for attempt in range(max_retries):
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
        break  # Exit the loop if the email is sent successfully

    except smtplib.SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error.decode()

        #continously try again after 1 minute.
        if error_code == 421:
            print(f"Attempt {attempt + 1}: Service not available, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Failed to send email: {error_message}")
            break  # Exit the loop for other errors

    except Exception as e:
        print(f"An error occurred: {e}")
        break

    finally:
        if server is not None:
            server.quit()  # Close the connection if it was established

else:
    print("Max retries reached. Failed to send the email.")
