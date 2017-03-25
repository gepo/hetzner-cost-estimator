Hetzner Costs Estimator
=======================

Intro
----

If you are hosting at hetzner.de then you know that Hetzner does not provide any cost estimation tools.

There are some reasons why you need to check how much your servers costs:

* You are under budget and is ordering/canceling servers, so you next invoice is not the same as previous.
* You want to review your expenses.

But Hetzner does not suggest anything useful for these tasks:
* There are no price for servers in account, you need to check it on homepage or get from server name (in case of server bought from bidding).
* You has many servers with addons, so you need to remember it or click on every server in web interface to check server addons. Obviously, prices for addons you should remember too.

It takes too much my time to check server and their addons prices, so I wrote script to parse their web interface and hetzner home page.
It get prices for yours servers from hetzner home page or server name, if it's from bidding. Also, it check addons for each server and list storage boxes.
It export to CSV next information about your account:

1. Servers (dedicated, vserver and managed) with their prices.
1. Paid addons for each server with their prices.
1. Storage boxes and their prices.

Installation
------------

You need python 2.7 or higher. Works on 3.5 also.

Install script dependencies:

```
pip install requests BeautifulSoup
```

Usage
-----

You can use it as follows:
```
./hetzner-costs.py <username> <password>
```

where username/password are your credentials for Hetzner Robot web interface.

Sample output of the script:
```
title;id;product;label;count;price;total
StorageBox;123456;BX50;;1;21.9;21.9
Server;100001;SB38;elastic-1.ex.com;1;31.9328;31.9328
Server;100002;SB39;elastic-2.ex.com;1;32.7731;32.7731
Server;100003;EX41-SSD;mongo-1.ex.com;1;39.0;39.0
Addon for Server;100003;FlexiPack;mongo-1.ex.com;1;12.61;12.61
Addon for Server;100003;960 GB 6 Gb/s SSD Datacenter Edition;mongo-1.ex.com;1;40.0;40.0
Server;100004;EX41-SSD;mongo-2.ex.com;1;39.0;39.0
217.2159
```

According to this output you have 1 storage box, 4 servers, one server has 2 addons - FlexiPack and 960GB SSD.
Total costs for it is 217.2159 EUR excluding VAT.

Total cost with VAT 19% can be easily calculated from these prices.
For this example it is 258.4869 EUR incl. VAT 19%.

It doesn't calculate exact invoice sum according server orderding date.
It always use full price, so use it only for costs estimation, not for exactly calculating your future invoice.