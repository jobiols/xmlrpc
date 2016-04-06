# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Script to check product prices
import xmlrpclib

from  server_access.server_data import DATABASE, SERVER, USERNAME, PASSWORD



# donde están los datos
CSVFILE = 'precios_mila.csv'
csv_default_code = 0
csv_name = 1
csv_list_price = 2

csv_sale_ok = 2

csv_purchase_ok = 3
csv_type = 4  # [product consu, service]
csv_categ_id = 6
csv_taxes_id = 7
csv_supplier_taxes_id = 8
csv_property_account_income = 9
csv_property_account_expense = 10

print "-------------------------------------"
print "checking database", DATABASE

sock_common = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/common')
uid = sock_common.login(DATABASE, USERNAME, PASSWORD)
sock = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/object')

# todos los productos de mila (marzi y pro)
record_ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', [
    '|', ('categ_id', '=', 25), ('categ_id', '=', 26)
])
products = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', record_ids,
                        ['default_code'])

print 'me traje todos los productos'

# para cada producto revisar si esta duplicado
for pro in products:
    record_ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', [
        ('default_code', '=', pro['default_code'])
    ])
    if len(record_ids) > 1:
        print record_ids, pro['default_code']
