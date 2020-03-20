from django.core.mail import send_mail, EmailMessage
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from django.urls import set_script_prefix
from django.utils import timezone

from microlearning.models import Profile, Article
from olgaproject.settings import EMAIL_HOST_USER, SITE_URL


class Command(BaseCommand):
    help = 'Send emails to subscribers'

    def handle(self, *args, **kwargs):
        set_script_prefix(SITE_URL)

        subject = 'OlgaProject: daily article subs!'

        category_users = {}
        for profile in Profile.objects.all():
            if profile.subscribed_category:
                category_users.setdefault(profile.subscribed_category, []).append(profile.user.email)

        for subscribed_category in category_users:
            recipients = category_users[subscribed_category]
            articles = Article.objects.filter(type=subscribed_category, publish__date=timezone.now()).all()

            if len(articles):
                message = render_to_string('email/new_articles.html', {'articles': articles})

                email = EmailMessage(subject=subject, body=message, from_email=EMAIL_HOST_USER, to=recipients)
                email.content_subtype = 'html'
                email.send()
