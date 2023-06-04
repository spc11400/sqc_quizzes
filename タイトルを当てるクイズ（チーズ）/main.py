from lxml import etree
from requests import Session as Session_
from time import sleep
from urllib.parse import urljoin


GET_SLEEP = 5


class Session(Session_):
    def __init__(self, *args, get_sleep=GET_SLEEP, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_sleep = get_sleep
        def response(r, *args, **kwargs):
            r.raise_for_status()
            sleep(self.get_sleep)
        self.hooks['response'] = response

    def get_html(self, url):
        r = self.get(url)
        return etree.HTML(r.content.decode('utf-8'))


def get_cheeses():
    cheeses = {}
    with Session() as s:
        base = 'https://www.meg-snow.com'
        html = s.get_html(urljoin(base, '/cheeseclub/knowledge/jiten/term/'))
        hrefs = [a.get('href') for a in html.xpath('//a[@class="eqChild05"]')]
        for href in hrefs:
            html = s.get_html(urljoin(base, href))
            xpath = '//h1[@class="jiten-term-detail-mv_heading_title"]'
            h1 = html.xpath(xpath)[0]
            key = next(h1.itertext()).strip()
            xpath = '(//div[@class="jiten-term-detail-tab_contents"])[2]//p'
            p = html.xpath(xpath)[0]
            value = '\n'.join(
                text for text_ in p.itertext()
                if (text := text_.strip())
            )
            cheeses[key] = value
    return cheeses
