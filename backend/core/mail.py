from django.core.mail import send_mail
from django.template.loader import render_to_string
from decouple import config
from django.urls import reverse
from django.conf import settings


def send_activation_email(user):
    url = reverse('activate', args=(user.activation_token,))
    url = settings.SITE_URL + url
    msg_plain = render_to_string('core/email/activation.txt', {'activation_url': url})
    msg_html = render_to_string('core/email/activation.html', {'activation_url': url})

    send_mail(
        'Oil Pumpers: activate your account',
        msg_plain,
        config('EMAIL_FROM'),
        [user.email],
        html_message=msg_html,
    )
