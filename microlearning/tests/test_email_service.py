from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.test import TestCase

from microlearning.models import Article


class EmailTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.user.profile.subscribed_category = 'pediatrics'
        self.user.save()

    def test_email_sender_with_no_articles(self):
        call_command('email_sender')

        self.assertEqual(len(mail.outbox), 0)

    def test_email_sender_with_articles(self):
        self.article = Article.objects.create(title="Some title",
                                              status="new",
                                              type="pediatrics",
                                              id_med=9)

        call_command('email_sender')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Microlearning: Pediatrics daily new articles')
        self.assertEqual(mail.outbox[0].to, [self.user.email])
