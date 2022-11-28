from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            from_email=os.environ.get("EMAIL_FROM"),
            body=data["body"],
            to=[data['toemail']]

)
        email.send()            
        