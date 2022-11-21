from time import sleep

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse


@shared_task()
def send_user_email_task(token, email_id):
    """
    Sends an email when user is created
    """


    try:
        print(email_id,token)
        url=settings.BASE_URL + reverse('verify_token_api', kwargs={"token": token}),
        print(url)
        send_mail(
            subject='PyJWT Token',
            message=url,
            from_email=None,
            recipient_list=[email_id]

        )
        return "done"
    except:
        return str("incomplete")
