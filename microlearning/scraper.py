import requests
from django.utils.text import slugify
from lxml import html

from microlearning.models import Article


def remove_ads(body: str) -> str:
    lines = body.split('\n')
    clean_lines = [line.strip() for line in lines if not line.strip().startswith('webmd')]

    return '\n'.join(clean_lines)


class MedscapeScraper(object):
    base_url = 'https://www.medscape.com/'

    def __init__(self):
        pass

    def get_articles_by_category(self, category: str) -> list:
        page = requests.get(self.base_url + category)
        tree = html.fromstring(page.text)

        # try to find View All link
        view_all_element = tree.cssselect('section.latest_news h2.section-title a')
        if len(view_all_element) == 0 or \
                view_all_element[0].text_content() != 'View All':
            raise Exception('Link "View All" not found :(')

        view_all_url = view_all_element[0].attrib['href']
        page = requests.get(self.base_url + view_all_url)
        tree = html.fromstring(page.text)

        # try to find articles
        article_elements = tree.cssselect('div#archives ul > li')

        articles = []
        for article in article_elements:
            link = article.find('a')
            title = link.text_content()
            url = link.attrib['href'][len('//www.medscape.com'):]
            if not url.startswith('/viewarticle'):
                continue

            id_med = int(url[len('/viewarticle/'):])
            teaser = article.cssselect('span.teaser')
            if len(teaser):
                teaser = teaser[0].text_content()
            else:
                teaser = None

            author = article.cssselect('div.byline > i')
            if len(author):
                author = author[0].text_content()
            else:
                author = 'Unknown'

            articles.append({
                'id_med': id_med,
                'title': title,
                'url': url,
                'author': author,
                'body': teaser,
            })

        return articles

    def get_full_article_by_url(self, url: str) -> dict:
        page = requests.get(self.base_url + url)
        tree = html.fromstring(page.text)

        title = tree.cssselect('h1.title')[0].text_content()
        id_med = int(url[len('/viewarticle/'):])
        author = tree.cssselect('p.meta-author')
        if len(author):
            author = author[0].text_content()
        else:
            author = 'Unknown'
        body = tree.cssselect('div#article-content')[0].text_content()
        body = remove_ads(body)

        return {
            'id_med': id_med,
            'title': title,
            'url': url,
            'author': author,
            'body': body,
        }


def create_article(data: dict, category: str) -> Article:
    article = Article()
    article.id_med = data['id_med']
    article.title = data['title']
    article.slug = slugify(article.title, allow_unicode=False)
    article.body = data['body']
    article.type = category
    article.author = data['author']

    return article
