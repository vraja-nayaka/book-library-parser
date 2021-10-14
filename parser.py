import requests
from bs4 import BeautifulSoup
import csv
import re

CARD_URL = 'https://stat.rgdb.ru/component/method/'
CARD_PARAMS = {'view': 'library', 'Itemid': '0', 'id': '28041'}

LIST_URL = 'https://stat.rgdb.ru/'
LIST_PARAMS = {'filter_federal': '5',
               'filter_type': '0',
               'filter_region': '71',
               'filter_level': '0',
               'filter_area': '0',
               'filter_finance': '0',
               'view': 'libraries'}
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://stat.rgdb.ru'
FILE = '/Users/vadim/Documents/libraries.csv'

REQUIRED_FIELDS = ['Почтовый адрес', 'Телефон',
                   'Наименование ЦБС', 'Руководитель библиотеки', 'E-mail']
WRITE_FIELDS = ['Ссылка', 'Адрес', 'Телефон',
                'Наименование', 'Руководитель библиотеки', 'E-mail']

CARDS_BY_PAGE = 30


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_card_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    anchers = soup.select('td > a')
    urls = []

    for ancher in anchers:
        urls.append(HOST + ancher.get('href'))

    return urls


def get_card_page_content(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    content = [url]

    for required_field in REQUIRED_FIELDS:
        labels = soup.find_all('th', string=re.compile(required_field))
        result_fields = set()

        for label in labels:
            label_text = label.find_next_sibling().get_text()
            prepared_text = label_text.replace('\n', '').replace('  ', '')

            if prepared_text != '' and prepared_text != ' ':
                result_fields.add(prepared_text)

        content.append(', '.join(result_fields))

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
        writer.writerow(WRITE_FIELDS)
        for item in items:
            writer.writerow(item)


def parse():
    first_list_html = get_html(
        LIST_URL, params={**LIST_PARAMS, **{'start': '0'}})
    if first_list_html.status_code == 200:
        info = []
        pages_count = get_pages_count(first_list_html.text)

        for page in range(1, pages_count + 1):
            start = page * CARDS_BY_PAGE
            print(f'Парсинг страницы {page} из {pages_count}... ({start})')
            params = {**LIST_PARAMS, **{'start': start}}

            list_html = first_list_html if page == 1 else get_html(
                LIST_URL, params=params)
            card_urls = get_card_urls(list_html.text)

            for card_url in card_urls:
                print('Обрабатываем: ' + card_url)
                card_html = get_html(card_url)
                info.append(get_card_page_content(card_html.text, card_url))

        save_file(info, FILE)
        print('Готово, файл сохранен: ', FILE)
    else:
        print('Error')


parse()
