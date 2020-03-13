import requests
from lxml import html


class MedscapeScraper(object):
    base_url = 'https://www.medscape.com/'

    def __init__(self):
        pass

    def get_articles_by_slug(self, slug: str) -> list:
        page = requests.get(self.base_url + slug)
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
        articles = []

        article_elements = tree.cssselect('div#archives ul > li')
        for article in article_elements:
            link = article.find('a')
            title = link.text_content()
            url = link.attrib['href'][len('//www.medscape.com'):]
            teaser = article.cssselect('span.teaser')
            if len(teaser) != 0:
                teaser = teaser[0].text_content()
            else:
                teaser = None
            author = article.cssselect('div.byline > i')[0].text_content()

            articles.append({
                'title': title,
                'url': url,
                'teaser': teaser,
                'author': author,
            })

        return articles
