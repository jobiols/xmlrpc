# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Script to download product prices

import csv
import xmlrpclib
from  server_access.server_data import DATABASE, SERVER, USERNAME, PASSWORD

# donde están los datos
CSVFILE = 'product_download_prices.csv'
csv_default_code = 0
csv_name = 1
csv_sale_ok = 2
csv_purchase_ok = 3
csv_type = 4  # [product consu, service]
csv_list_price = 5
csv_categ_id = 6
csv_taxes_id = 7
csv_supplier_taxes_id = 8
csv_property_account_income = 9
csv_property_account_expense = 10


print "-------------------------------------"
print "downloading data from", DATABASE

# devuelve un writer para escribir un archivo csv sin quotas
def write_csv(filename):
    writer = csv.writer(open(filename, 'wb'), delimiter=',', quotechar='',
                        quoting=csv.QUOTE_NONE)
    return writer

sock_common = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/common')
uid = sock_common.login(DATABASE, USERNAME, PASSWORD)
sock = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/object')

reader = csv.reader(open(CSVFILE, 'rb'))


def categ_to_id(categ):
    if categ == 'Kryolan':
        ret = 39
    return ret


args = [('categ_id', '=', categ_to_id('Kryolan'))]
ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', args)
fields = ['default_code', 'list_price', 'name']
data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', ids, fields)
r = write_csv(CSVFILE)
for d in data:
    print(d)
