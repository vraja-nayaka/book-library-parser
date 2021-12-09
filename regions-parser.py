import requests
from bs4 import BeautifulSoup
import csv
import re

CARD_URL = 'https://stat.rgdb.ru/component/method/'
CARD_PARAMS = {'view': 'library', 'Itemid': '0', 'id': '28041'}

LIST_URL = 'https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B9%D0%BE%D0%BD%D1%8B_%D1%81%D1%83%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}

FILE = '/Users/vadim/Documents/regions/regions.csv'

REQUIRED_FIELDS = ['Почтовый адрес', 'Телефон',
                   'Наименование ЦБС', 'Руководитель библиотеки', 'E-mail']
WRITE_FIELDS = ['Ссылка', 'Адрес', 'Телефон',
                'Наименование', 'Руководитель библиотеки', 'E-mail']


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_regions(table):
    anchers = table.select('td:first-child a:first-child')
    sub_regions_ols = table.select('td:nth-child(6) ol')

    titles = []

    # for ancher in anchers:
    for index in range(0, min(len(anchers), len(sub_regions_ols))):
        title = anchers[index].get('title')
        sub_region_ol = sub_regions_ols[index]
        sub_regions = sub_region_ol.select('li a:first-child')

        sub_region_titles = []
        for sub_region_anchor in sub_regions:
            sub_region_titles.append(sub_region_anchor.get('title'))

        if title and sub_region_titles:
            dict = {'title': title, 'sub': sub_region_titles}
            titles.append(dict)

    print(titles)

    return titles


# def get_card_page_content(html, url):
#     soup = BeautifulSoup(html, 'html.parser')
#     content = [url]

#     for required_field in REQUIRED_FIELDS:
#         labels = soup.find_all('th', string=re.compile(required_field))
#         result_fields = set()

#         for label in labels:
#             label_text = label.find_next_sibling().get_text()
#             prepared_text = label_text.replace('\n', '').replace('  ', '')

#             if prepared_text != '' and prepared_text != ' ':
#                 result_fields.add(prepared_text)

#         content.append(', '.join(result_fields))

#     return content


def get_tables(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_='wikitable')
    return tables


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';', dialect='excel')
        writer.writerow(WRITE_FIELDS)
        for item in items:
            writer.writerow(item)


def parse():
    list_html = get_html(LIST_URL)
    if list_html.status_code == 200:
        info = []
        tables = get_tables(list_html.text)

        for table in tables:
            regions = get_regions(table)
            # print(regions)

        # print(f'Парсинг страницы {page} из {pages_count}... ({start})')
        # params = {**LIST_PARAMS, **{'start': start}}

        # list_html = list_html if page == 1 else get_html(
        #     LIST_URL, params=params)
        # card_urls = get_card_urls(list_html.text)

        # for card_url in card_urls:
        #     print('Обрабатываем: ' + card_url)
        #     card_html = get_html(card_url)
        #     info.append(get_card_page_content(card_html.text, card_url))

        # save_file(info, FILE)
        print('Готово, файл сохранен: ', FILE)
    else:
        print('Error')


parse()
