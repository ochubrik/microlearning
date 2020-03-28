from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from django.urls import set_script_prefix, clear_script_prefix
from django.utils import timezone

from microlearning.models import Profile, Article
from olgaproject.settings import EMAIL_HOST_USER, SITE_URL


class Command(BaseCommand):
    help = 'Send emails to subscribers'

    def handle(self, *args, **kwargs):
        set_script_prefix(SITE_URL)

        category_users = {}
        for profile in Profile.objects.all():
            if profile.subscribed_category:
                category_users.setdefault(profile.subscribed_category, []).append(profile.user.email)

        for subscribed_category in category_users:
            recipients = category_users[subscribed_category]
            articles = Article.objects.filter(type=subscribed_category, publish__date=timezone.now()).all()

            if len(articles):
                subject = 'Microlearning: {} daily new articles'\
                    .format(dict(Article.ARTICLE_TYPES).get(subscribed_category))

                message = render_to_string('email/new_articles.html', {'articles': articles})

                for recipient in recipients:
                    email = EmailMessage(subject=subject, body=message, from_email=EMAIL_HOST_USER, to=[recipient])
                    email.content_subtype = 'html'
                    email.send()

        clear_script_prefix()
