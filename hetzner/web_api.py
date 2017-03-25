import requests
from bs4 import BeautifulSoup

class HetznerWebAPI:
    def __init__(self):
        # self.jar = CookieJar()
        self.session = requests.session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def login(self, username, password):
        # FIXME: use cookiejar persisted at file
        self.session.get('https://robot.your-server.de/')
        resp = self.session.post('https://robot.your-server.de/login/check',
                                 data={'user': username, 'password': password})
        return 200 == resp.status_code

    def listServers(self):
        resp = self.session.get('https://robot.your-server.de/server')
        soup = BeautifulSoup(resp.text, 'html.parser')

        servers = list()

        for server_row in soup.find_all('table', class_='box_title'):
            server_title = server_row.find('span', class_='tooltip_underline').text
            spans = server_row.find('td', class_='title').find_all('span')
            # example: EX40-SSD (30 TB) #123456
            parts = server_title.split(' ')

            cancelled = False
            if len(spans) > 1:
                img = spans[1].find('img')

                if img != None:
                    cancelled = img['src'] == '/images/cancelled.png'

            label_elem = server_row.find('td', class_='server_name').find('span', class_='server_name_input')
            if label_elem != None:
                label = label_elem.text
            else:
                label = None

            servers.append({
                'id': parts[3][1:],
                'product': parts[0],
                'cancelled': cancelled,
                'label': label,
            })

        return servers

    def listStorageBoxes(self):
        resp = self.session.get('https://robot.your-server.de/storage')
        soup = BeautifulSoup(resp.text, 'html.parser')

        boxes = list()

        for box_row in soup.find_all('table', class_='box_title'):
            box_title = box_row.find('td', class_='title').text
            parts = box_title.split(' ')
            boxes.append({
                'id': parts[1][1:],
                'product': parts[0],
            })
        return boxes

    def serverAddons(self, id):
        resp = self.session.post('https://robot.your-server.de/server/data/id/' + str(id),
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