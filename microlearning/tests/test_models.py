from django.contrib.auth import get_user_model
from django.test import TestCase

from microlearning.models import Article


class TestArticle(TestCase):

    def setUp(self):
        self.article_first = Article.objects.create(
            id_med=1,
            title="Some title",
            type="some_str",
        )

    def test_article_is_assigned_slug(self):
        self.assertEqual(self.article_first.slug, 'some-title')

    def test_get_absolute_url(self):
        self.assertEqual('/microlearning/some_str/1-some-title', self.article_first.get_absolute_url())


class TestProfile(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.article = Article.objects.create(title="Some title",
                                              status="new",
                                              type="pediatrics",
                                              id_med=9)

    def test_get_my_articles_empty_list(self):
        self.profile = self.user.profile
        self.profile.subscribed_category = 'neurology'

        self.assertEqual(list(self.profile.get_my_articles()), [])

    def test_get_my_articles_list(self):
        self.profile = self.user.profile
        self.profile.subscribed_category = 'pediatrics'

        self.assertEqual(self.profile.subscribed_category, 'pediatrics')
        self.assertEqual(list(self.profile.get_my_articles()), [self.article])
