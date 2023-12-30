from django.core.mail import EmailMessage
from portfolio_cum_blog import settings


def test_send_email(request):
    email_message = EmailMessage(
        'This is the subject',
        'This is the message',
        settings.APPLICATION_EMAIL,
        ['gautam.ku.ecom@gmail.com'],
        reply_to=settings.APPLICATION_EMAIL
    )
    email_message.send(fail_silently=False)
