import requests
from bs4 import BeautifulSoup
import csv
import unicodedata

url = 'https://televize.heureka.cz/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'accept': '*/*'}


def get_html(url):
    print(url)
    r = requests.get(url, headers=headers)
    return r


def get_pages(html):
    return 71


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('li', class_='c-product-list__item')
    autos = []
    for item in items:
        try:
            price_min = item.find('a', class_='c-product__price').find('span').find('span').get_text(strip=True)
            price_max = item.find('a', class_='c-product__price').find('span').findAll('span')[2].get_text(
                    strip=True)
        except AttributeError:
            price_min = item.find('a', class_='c-product__price').find('span').get_text(strip=True)
            price_max = 'no max price'
        autos.append({
            'type': 'Televisor',
            'brand': item.find('a', class_='c-product__link').get_text(
                strip=True).split(' ')[0],
            'model': item.find('a', class_='c-product__link').get_text(
                strip=True).split(' ')[1],
            'price_min': price_min,
            'price_max': price_max,
            'numbers': item.find('a', class_='c-product__shops c-product__link').find('span').get_text(strip=True),
            'link': item.find('a', class_='c-product__link').get('href')
        })
        print(autos)
    return autos


def save(items):
    with open('turkcatalog.csv', 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Type product', 'Brand', 'Model', 'Min price', 'Max price', 'Num offers', 'URL'])
        for auto in items:
            writer.writerow(
                [auto['type'], auto['brand'], auto['model'], unicodedata.normalize("NFKD", auto['price_min']),
                 unicodedata.normalize("NFKD", str(auto['price_max'])),
                 auto['numbers'],
                 auto['link']])


def parse():
    html = get_html(url)
    if html.status_code == 200:
        autos = []
        pages_count = get_pages(html.text)
        i = 0
        for page in range(1, pages_count + 1):
            i+=1
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(f'https://televize.heureka.cz/?f={i}')
            autos.extend(get_content(html.text))
            save(autos)
        print(f'Получено {len(autos)} автомобилей')
    else:
        print('error')


parse()
