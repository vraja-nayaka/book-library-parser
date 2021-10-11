import requests
from bs4 import BeautifulSoup
import csv

CARD_URL = 'https://stat.rgdb.ru/component/method/'
CARD_PARAMS = {'view': 'library', 'Itemid': '0', 'id': '28041'}

LIST_URL = 'https://stat.rgdb.ru/?filter_federal=5&filter_type=0&filter_region=71&filter_level=0&filter_area=0&filter_finance=0&view=libraries&start=0'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://stat.rgdb.ru'
FILE = '/Users/vadim/Documents/libraries.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_card_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    anchers = soup.select('td > a')
    urls = []

    for ancher in anchers:
        urls.append(HOST + ancher.get('href'))

    return urls


def get_card_page_content(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    library_tds = soup.find_all('td')
    content = []

    for item in library_tds:
        content.append(item.get_text().replace('\n', '').replace('  ', ''))
        content[0] = url

    return content


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('li', class_='hidden-phone')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';', dialect='excel')
        writer.writerow(['Ссылка', 'Адрес', 'Телефон',
                        'Наименование', 'Руководитель библиотеки', 'E-mail'])
        for item in items:
            writer.writerow([item[0], item[10], item[11] + ', ' +
                            item[15], item[12], item[14], item[13] + ' ' + item[15]])


def parse():
    list_html = get_html(LIST_URL)
    print(list_html.status_code)
    if list_html.status_code == 200:
        card_urls = get_card_urls(list_html.text)
        info = []
        pages_count = get_pages_count(list_html.text)
        print(pages_count)

        for card_url in card_urls:
            print('starting on: ' + card_url)
            card_html = get_html(card_url)
            info.append(get_card_page_content(card_html.text, card_url))

        save_file(info, FILE)
    else:
        print('Error')


parse()
