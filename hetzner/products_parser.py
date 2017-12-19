# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup

def parse():
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'https://github.com/gepo/hetzner-cost-estimator'})

    def to_float(v):
        try:
            return float(v.replace(',', '.'))
        except ValueError:
            return None

    def _parseDedicated():
        data = sess.get('https://www.hetzner.de/dedicated-rootserver/getServer').json()

        return { srv['name']: to_float(srv['price_v']) for srv in data['server'] }

    def _parseProductPage(url):
        soup = BeautifulSoup(sess.get(url).text, 'html.parser')

        product_table = soup.find('table', class_='product-overview-card')
        map = {}

        product_names = list()
        for item in product_table.find('thead').find_all('a'):
            product_names.append(item.contents[0])

        index = 0
        for item in product_table.find('tbody').find('tr').find_all('span'): 
            if '€' != item.text[0]:
                continue

            product_name = product_names[index]
            index += 1
            map[product_name] = to_float(item.text[2:])

        return map

    def _parseVserver():
        return _parseProductPage('https://www.hetzner.de/virtual-server')

    def _parseManaged():
        return _parseProductPage('https://www.hetzner.de/managed-server')

    def _parseBox():
        return _parseProductPage('https://www.hetzner.de/storage-box')

    def _parseFlexiPack():
        soup = BeautifulSoup(sess.get('https://www.hetzner.de/flexipack').text, 'html.parser')

        map = {}
        map['FlexiPack'] = to_float(
            soup
                .find('div', class_='product-order-sidebar')
                .find('div', class_='price')
                .text[2:]
            )

        for row in soup.find('table', class_='table-overview').find_all('tr'):
            name = row.find('td').text
            price = to_float(row.find_all('td')[1].text[2:])

            if price is None:
                continue

            map[name] = price

        return map

    return {
        'dedicated': _parseDedicated(),
        'vserver': _parseVserver(),
        'managed': _parseManaged(),
        'box': _parseBox(),
        'addon': _parseFlexiPack()
    }
