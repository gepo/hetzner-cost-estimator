# -*- coding: utf8 -*-
import requests
import math
from bs4 import BeautifulSoup

class HetznerWebAPI:
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers.update({'User-Agent': 'https://github.com/gepo/hetzner-cost-estimator'})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sess.close()

    def login(self, username, password):
        # FIXME: use cookiejar persisted at file
        self.sess.get('https://robot.your-server.de/')
        resp = self.sess.post('https://accounts.hetzner.com/login_check',
                                 data={'_username': username, '_password': password})
        return 200 == resp.status_code

    def listServers(self):
        resp = self.sess.get('https://robot.your-server.de/server')
        soup = BeautifulSoup(resp.text, 'html.parser')

        totalServers = int(soup.find('span', class_='box_count').find('span').text)
        pages = math.ceil(totalServers / 50)

        servers = list(self._parseServersPage(soup))

        for page in range(2, pages+1):
            resp = self.sess.get('https://robot.your-server.de/server/index/page/' + str(page))
            soup = BeautifulSoup(resp.text, 'html.parser')
            for server in self._parseServersPage(soup):
                servers.append(server)
            
        return servers

    def _parseServersPage(self, soup):
        for server_row in soup.find_all('table', class_='box_title'):
            # example: EX40-SSD (30 TB) #123456
            parts = server_row.find('span', class_='tooltip_underline').text.split(' ')
            productId, productCode = parts[3][1:], parts[0]

            spans = server_row.find('td', class_='title').find_all('span')
            img = spans[1].find('img') if len(spans) > 1 else None
            cancelled = img['src'] == '/images/cancelled.png' if img is not None else False

            label_elem = server_row.find('td', class_='server_name').find('span', class_='server_name_input')
            label = label_elem.text if label_elem is not None else None

            yield {
                'id': productId,
                'product': productCode,
                'cancelled': cancelled,
                'label': label,
            }

    def listStorageBoxes(self):
        resp = self.sess.get('https://robot.your-server.de/storage')
        soup = BeautifulSoup(resp.text, 'html.parser')

        boxes = list()

        for box_row in soup.find_all('table', class_='box_title'):
            parts = box_row.find('td', class_='title').text.split(' ')
            boxId, boxCode = parts[1][1:], parts[0]

            boxes.append({
                'id': boxId,
                'product': boxCode,
            })
            
        return boxes

    def serverAddons(self, id):
        resp = self.sess.post('https://robot.your-server.de/server/data/id/' + str(id),
                                 headers={'X-Requested-With': 'XMLHttpRequest'})
        soup = BeautifulSoup(resp.text, 'html.parser')

        addons = list()

        for row in soup.find_all('tr'):
            cols = row.find_all('td')

            name = cols[1].text
            if 'Reset service' == name:
                continue

            addons.append({
                'count': int(cols[0].text.split(' ')[0]),
                'name': name,
            })

        return addons
