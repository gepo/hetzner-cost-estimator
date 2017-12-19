# -*- coding: utf8 -*-

from collections import namedtuple
from hetzner import products_parser
from hetzner.web_api import HetznerWebAPI

class ProductPriceGuesser:
    def __init__(self):
        pass

    def set_products(self, products):

        self.servers = {}
        self.servers.update(products['vserver'])
        self.servers.update(products['dedicated'])
        self.servers.update(products['managed'])

        self.addon = products['addon']
        self.box = products['box']

    def guess_server_price(self, product):
        if product.startswith('SB'):
            return round(float(product[2:]) / 1.19, 4)

        if product in self.servers:
            return self.servers[product]

        return None

    def guess_addon_price(self, addon_name):
        if addon_name in self.addon:
            return self.addon[addon_name]

        addon_name = addon_name.replace('GB ', 'GB SATA ')
        if addon_name in self.addon:
            return self.addon[addon_name]

        return None

    def guess_box_price(self, box_name):
        if box_name in self.box:
            return self.box[box_name]

        return None

ItemInfo = namedtuple('ItemInfo', 'title id product label count price total')

def estimate_costs(username, password):
    price_guesser = ProductPriceGuesser()
    price_guesser.set_products(products_parser.parse())
    
    api = HetznerWebAPI()
    if not api.login(username, password):
        raise "Invalid login or password"

    boxes = api.listStorageBoxes()
    for box in boxes:
        price = price_guesser.guess_box_price(box['product'])
        yield ItemInfo(
            title='StorageBox',
            id=box['id'],
            product=box['product'],
            label=None,
            count=1,
            price=price,
            total=price,
        )

    servers = api.listServers()
    for srv in servers:
        if srv['cancelled']:
            continue

        price = price_guesser.guess_server_price(srv['product'])

        yield ItemInfo(
            title='Server',
            id=srv['id'],
            product=srv['product'],
            label=srv['label'],
            count=1,
            price=price,
            total=price,
        )

        for addon in api.serverAddons(srv['id']):
            price = price_guesser.guess_addon_price(addon['name'])

            total = None
            if price is not None:
                total = addon['count'] * price

            yield ItemInfo(
                title='Addon for Server',
                id=srv['id'],
                product=addon['name'],
                label=srv['label'],
                count=addon['count'],
                price=price,
                total=total,
            )