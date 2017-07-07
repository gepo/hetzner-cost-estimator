import requests
from bs4 import BeautifulSoup

def parse():
    res = {}
    res.update(_parseServerProducts())
    res.update({'addon': _parseFlexiPack()})

    return res

def _parseServerProducts():
    map = {
        'dedicated': _parseDedicated(),
        'vserver': _parseVserver(),
        'managed': _parseManaged(),
        'box': _parseBox(),
    }
    return map

def _parseDedicated():
    url = 'https://www.hetzner.de/dedicated-rootserver/getServer'
    data = _request(url).json()

    return { srv['name']: float(srv['price_v'].replace(',', '.')) for srv in data['server'] }

def _parseProductPage(url):
    resp = _request(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

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
        map[product_name] = float(item.text[2:].replace(',', '.'))

    return map

def _parseVserver():
    return _parseProductPage('https://www.hetzner.de/virtual-server')

def _parseManaged():
    return _parseProductPage('https://www.hetzner.de/managed-server')

def _parseBox():
    return _parseProductPage('https://www.hetzner.de/storage-box')

def _parseFlexiPack():
    resp = _request('https://www.hetzner.de/flexipack')
    soup = BeautifulSoup(resp.text, 'html.parser')

    map = {}
    map['FlexiPack'] = float(
        soup.find('div', class_='product-order-sidebar').find('div', class_='price').text[2:].replace(',', '.'))

    for row in soup.find('table', class_='table-overview').find_all('tr'):
        name = row.find('td').text

        price_str = row.find_all('td')[1].text[2:]
        try:
            price = float(price_str.replace(',', '.'))
        except ValueError:
            continue

        map[name] = price

    return map

def _request(url):
    return requests.get(url, headers={'User-Agent': 'https://github.com/gepo/hetzner-cost-estimator'})
