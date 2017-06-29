import requests
from bs4 import BeautifulSoup

def parse():
    res = {}
    res.update(_parseServerProducts())
    res.update({'addon': _parseFlexiPack()})

    return res

def _parseServerProducts():
    resp = requests.get('http://hetzner.de/de')
    soup = BeautifulSoup(resp.text, 'html.parser')

    map = {
        'dedicated': _parseDedicated(),
        'vserver': _parseVserver(soup),
        'managed': _parseManaged(soup),
        'box': _parseBox(soup),
    }
    return map

def _parseDedicated():
    url = 'https://www.hetzner.de/dedicated-rootserver/getServer'
    data = requests.get(url).json()

    return { srv['name']: float(srv['price_v']) for srv in data['server'] }

def _parseVserver(soup):
    return {} # FIXME
    map = {}

    for item in soup.find_all('li', class_='tded')[1].find_all('li'):

        a_item = item.find('a')
        if a_item is None:
            continue

        product_name = a_item.contents[0][8:].rstrip(' ')

        price_elem = a_item.find('font', class_='klapp_preise')
        if price_elem is None:
            continue

        price_elem = price_elem.find('noscript')
        if price_elem is None:
            continue

        map[product_name] = float(price_elem.text.replace(',', '.'))

    return map

def _parseManaged(soup):
    return {} # FIXME
    map = {}

    for item in soup.find_all('li', class_='mded')[0].find_all('li'):

        a_item = item.find('a')
        if a_item is None:
            continue

        product_name = a_item.contents[0]

        price_elem = a_item.find('font', class_='klapp_preise')
        if price_elem is None:
            continue

        price_elem = price_elem.find('noscript')
        if price_elem is None:
            continue

        map[product_name] = float(price_elem.text.replace(',', '.'))

    return map

def _parseBox(soup):
    return {} # FIXME
    map = {}

    for item in soup.find_all('li', class_='support')[0].find_all('ul')[0].find_all('li'):

        a_item = item.find('a')
        if a_item is None:
            continue

        product_name = a_item.contents[0].rstrip(' ')

        price_elem = a_item.find('font', class_='klapp_preise')
        if price_elem is None:
            continue

        price_elem = price_elem.find('noscript')
        if price_elem is None:
            continue

        map[product_name] = float(price_elem.text.replace(',', '.'))

    return map

def _parseFlexiPack():
    return {} # FIXME
    resp = requests.get('https://www.hetzner.de/de/hosting/produkte_rootserver/flexipack')
    soup = BeautifulSoup(resp.text, 'html.parser')

    map = {}
    map['FlexiPack'] = float(
        soup.find('div', class_='product-more').find('strong').find('noscript').text.replace(',', '.'))

    for row in soup.find('div', class_='table-holder').find_all('tr', class_='noborder'):
        name = row.find('td', class_='name').text
        price_cell = row.find('td', class_='SH-5').find('strong')
        if price_cell is None:
            continue
        price_cell = price_cell.find('noscript') or price_cell

        price = float(price_cell.text.replace(',', '.'))

        map[name] = price

    return map
