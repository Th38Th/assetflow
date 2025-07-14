import logging
import os
import smtplib
from email.mime.text import MIMEText

SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
SERVER_PORT = os.getenv("SERVER_PORT")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def send_email(recipient_email: str, subject: str, body: str):
    html_message = MIMEText(body, 'html')
    html_message["Subject"] = subject
    html_message["From"] = SENDER_EMAIL
    html_message["To"] = recipient_email
    with smtplib.SMTP_SSL(SERVER_ADDRESS, SERVER_PORT) as server:
        logging.info(f"SMTP connection to [{SERVER_ADDRESS}:{SERVER_PORT}] established")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, html_message.as_string())
        logging.info(f"Sent [{subject}] email to [{recipient_email}]")

def send_welcome_email(recipient_email: str, recipient_username: str):
    message = """
<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Welcome</title>
  <style>
    body, table, td, a {
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }
    table, td {
      mso-table-rspace: 0pt;
      mso-table-lspace: 0pt;
    }
    img {
      -ms-interpolation-mode: bicubic;
      border: 0;
      height: auto;
      line-height: 100%;
      outline: none;
      text-decoration: none;
      max-width: 100%;
      display: block;
    }
    body {
      margin: 0;
      padding: 0;
      width: 100% !important;
      background-color: #f7f7f7;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .container {
      max-width: 600px;
      margin: 0 auto;
      background-color: #ffffff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .header {
      background-color: #4f46e5;
      padding: 20px;
      color: white;
      text-align: center;
      font-size: 24px;
      font-weight: 700;
    }
    .content {
      padding: 30px 40px;
      color: #333333;
      font-size: 16px;
      line-height: 1.5;
    }
    .content h1 {
      margin-top: 0;
      color: #111827;
    }
    .button {
      display: inline-block;
      margin-top: 25px;
      padding: 12px 24px;
      background-color: #4f46e5;
      color: white !important;
      text-decoration: none;
      border-radius: 6px;
      font-weight: 600;
      font-size: 16px;
    }
    .footer {
      font-size: 12px;
      color: #888888;
      text-align: center;
      padding: 20px 10px;
    }
    @media screen and (max-width: 640px) {
      .container {
        width: 90% !important;
        padding: 0;
      }
      .content {
        padding: 20px;
      }
      .header {
        font-size: 20px;
      }
    }
  </style>
</head>
<body>
  <table width="100%" bgcolor="#f7f7f7" cellpadding="0" cellspacing="0" role="presentation">
    <tr>
      <td align="center">
        <table class="container" role="presentation" cellpadding="0" cellspacing="0">
          <tr>
            <td class="header">
              Welcome to AssetFlow!
            </td>
          </tr>
          <tr>
            <td class="content">
              <h1>Hello, <b>"""+recipient_username+"""</b>, and welcome!</h1>
              <p>
                Thank you for joining AssetFlow. We're excited to have you on board.
              </p>
              <p>
                With AssetFlow, managing your digital assets becomes seamless and effortless.
              </p>
              <p>
                If you have any questions or need assistance, just reply to this email — we're here to help!
              </p>
              <p>Best regards,<br/>The AssetFlow Team</p>
            </td>
          </tr>
          <tr>
            <td class="footer">
              &copy; 2025 AssetFlow. All rights reserved.<br/>
              You received this email because you signed up for AssetFlow.
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
    """
    send_email(recipient_email, "Welcome to AssetFlow", message)