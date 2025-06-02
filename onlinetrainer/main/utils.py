from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

def send_confirmation_email(user, request):
    user.is_active = False
    user.save()

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    current_site = get_current_site(request)
    activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

    subject = "Підтвердження електронної пошти"
    text_content = f"Привіт, {user.username}!\nПерейдіть за посиланням на сайт для активації акаунту:\n{activation_link}"
    html_content = render_to_string(
        'main/activation_email.html',
        {'username': user.username, 'activation_link': activation_link}
    )

    msg = EmailMultiAlternatives(subject, text_content, None, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

    print("=== Лист надіслано (HTML) ===")

