from django.test import SimpleTestCase
from django.urls import reverse, resolve

from microlearning.views import article_details, article_index,\
    article_list, settings, register, edit, view_profile, change_password


class TestUrls(SimpleTestCase):

    def test_article_index(self):
        url = reverse('microlearning:article_index')
        self.assertEqual(resolve(url).func, article_index)

    def test_article_details(self):
        url = reverse('microlearning:article_details', args=['some_str', 9, 'some_slug'])
        self.assertEqual(resolve(url).func, article_details)

    def test_article_list(self):
        url = reverse('microlearning:article_list')
        self.assertEqual(resolve(url).func, article_list)

    def test_settings(self):
        url = reverse('microlearning:settings')
        self.assertEqual(resolve(url).func, settings)

    def test_register(self):
        url = reverse('microlearning:register')
        self.assertEqual(resolve(url).func, register)

    def test_edit(self):
        url = reverse('microlearning:edit')
        self.assertEqual(resolve(url).func, edit)

    def test_profile(self):
        url = reverse('microlearning:profile')
        self.assertEqual(resolve(url).func, view_profile)

    def test_password(self):
        url = reverse('microlearning:change_password')
        self.assertEqual(resolve(url).func, change_password)
