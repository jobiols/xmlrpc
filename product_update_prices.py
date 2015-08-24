# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Script to update product prices
# si el default_code existe lo actualiza, si no existe lo crea
import csv
import xmlrpclib

# donde están los datos
CSVFILE = 'product_update_prices.csv'
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

SERVER = 'http://makeover.sytes.net:8069'
DATABASE = 'makeover_datos'
USERNAME = 'admin'
PASSWORD = 'melquiades'
# raw_input('Enter password: ')

print "-------------------------------------"
print "updating database", DATABASE

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


for row in reader:
    values = {'default_code': row[csv_default_code],
              'name': row[csv_name],
              'sale_ok': row[csv_sale_ok],
              'purchase_ok': row[csv_purchase_ok],
              'type': row[csv_type],
              'list_price': row[csv_list_price],
              'categ_id': categ_to_id(row[csv_categ_id]),
              }

    args = [('default_code', '=', row[csv_default_code])]
    ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', args)

    if ids:
        # el codigo existe
        print 'codigo existe ', row
        data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'write', ids,
                            values)

    # fields = ['default_code','list_price','categ_id']
    #        data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', ids, fields)
    #        print(data)

    else:
        print 'codigo no existe ', row
        data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'create', values)
