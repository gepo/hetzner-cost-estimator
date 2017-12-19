#!/usr/bin/env python
# -*- coding: utf8 -*-

import csv
import sys

from hetzner.price import ItemInfo
from hetzner.price import estimate_costs

if len(sys.argv) != 3:
    sys.stderr.write("Usage:\n\t./hetzner-costs.py <username> <password>\n\n")
    sys.exit(1)

total = 0.0
writer = csv.writer(sys.stdout, delimiter='\t')
writer.writerow(ItemInfo._fields)

for item in estimate_costs(sys.argv[1], sys.argv[2]):
    writer.writerow(item)
    if item.total is not None:
        total += item.total

writer.writerow(['total_vat_excl'])
writer.writerow([round(total, 4)])
