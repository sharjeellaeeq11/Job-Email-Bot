import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def main():

    first_name = "<enter_first_name>"
    last_name = "<enter_last_name>"
    company = "<Company_name>"
    role = "<enter_role>"
    job_posting_url = "<job_URL>"

    email_permutation = generate_emails(first_name, last_name, company)

    subject = f"<Enter subject here>"
    body = f"""
    <p>Greetings {first_name}</p>
    <p>My name is XYZ and I graduated from UC Berkeley with a Masters degree in Mechanical Engineering.</p>
    <p>I just completed my internship and I just wanted to introduce myself as a potential candidate for the <a href="{job_posting_url}">{role}</a> role at {company}.</p>

    <p>Best,</p>
    <p>Your Name</p>
    """


    resume_path = "path where your resume lives"

    for i in email_permutation:
        send_email(first_name, last_name, company, subject, body, i, resume_path)


def send_email(first_name, last_name, company, subject, body, to_email, resume_path):
    # Email credentials
    sender_email = "your email"
    sender_password = "your password"

    # Setting up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body with MIMEText (HTML)
    msg.attach(MIMEText(body, 'html'))

    # Open the resume file in binary mode and attach it
    resume_name = os.path.basename(resume_path)
    with open(resume_path, "rb") as resume_file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(resume_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={resume_name}')
        msg.attach(part)

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to secure
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        print(f"Email sent to {first_name} {last_name} at {company} successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        server.quit()


def generate_emails(first_name, last_name, company):
    # Clean and lowercase inputs
    first_name = first_name.lower()
    last_name = last_name.lower()
    company = company.lower() + ".com"

    # Common email patterns
    email_patterns = [
        f"{first_name}.{last_name}@{company}",
        f"{first_name}@{company}",
        f"{first_name}{last_name}@{company}",
        f"{first_name}{last_name[0]}@{company}",
        f"{first_name[0]}{last_name}@{company}",
        f"{first_name}_{last_name}@{company}",
        f"{first_name[0]}.{last_name}@{company}",
        f"{last_name}.{first_name}@{company}",
        f"{last_name}@{company}",
        f"{last_name}{first_name[0]}@{company}",
    ]

    return email_patterns


if __name__ == "__main__":
    main()
