import smtplib
import ssl

port = 465  # For SSL
password = "pass"

# Create a secure SSL context
context = ssl.create_default_context()


def send(email, username, token):

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("mail@gmail.com", password)

        content = "Your password reset token is {}".format(
            token) + "\n" + "Please click on the link to reset your password http://localhost:8080/resetPassword?username=" + username + "&passwordToken=" + token + "&newPassword= and don't forget to add your new password to the link"

        server.sendmail("mail@gmail.com", email, content)
