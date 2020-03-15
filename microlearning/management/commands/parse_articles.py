from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from microlearning import scraper
from microlearning.models import Article


class Command(BaseCommand):
    help = 'Parse and save articles from medscape'

    def handle(self, *args, **kwargs):
        medscape_scraper = scraper.MedscapeScraper()

        for category, name in Article.ARTICLE_TYPES:
            self.stdout.write('Start parsing {} category'.format(name))

            articles = medscape_scraper.get_articles_by_category(category)

            self.stdout.write('Found {} articles'.format(len(articles)))

            added_count, not_unique_count = 0, 0
            for item in articles:
                article = scraper.create_article(item, category)

                try:
                    article.validate_unique()

                    parsed_article = medscape_scraper.get_full_article_by_url(item['url'])

                    article = scraper.create_article(parsed_article, category)
                    article.save()

                    added_count += 1
                except ValidationError:
                    not_unique_count += 1

            self.stdout.write('Added: {}. Not unique: {}'.format(added_count, not_unique_count))
