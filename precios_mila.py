# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Script to check product prices
import csv
import xmlrpclib

from  server_access.server_data import DATABASE, SERVER, USERNAME, PASSWORD



# donde están los datos
CSVFILE = 'precios_mila.csv'

csv_default_code = 0
csv_name = 1
csv_list_price = 2
csv_categ_id = 3

csv_sale_ok = 2
csv_purchase_ok = 3
csv_type = 4  # [product consu, service]
csv_taxes_id = 7
csv_supplier_taxes_id = 8
csv_property_account_income = 9
csv_property_account_expense = 10

print "-------------------------------------"
print "checking database", DATABASE

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
    if categ == 'MM':
        ret = 25
    if categ == 'MP':
        ret = 26
    return ret


def strip_code(code):
    return code[2:]


for row in reader:
    print row
    values = {'default_code': strip_code(row[csv_default_code]),
              'name': row[csv_name],
              'sale_ok': True,
              'purchase_ok': True,
              'list_price': row[csv_list_price],
              'categ_id': categ_to_id(row[csv_categ_id]),
              'type': 'product'
              }

    args = [('default_code', '=', strip_code(row[csv_default_code]))]
    ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', args)

    if len(ids) > 1:
        print 'duplicate ---------------', ids, row
        exit(1)

    if ids:
        # el codigo existe
        #        data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', ids, values)
        #        print 'existe', row
        #        print '//',row[csv_name],'//', data[0]['name'],'//'
        #        print 'codigo existe ', row
        data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'write', ids,
                            values)

    # fields = ['default_code','list_price','categ_id']
    #        data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', ids, fields)
    #        print(data)

    else:
        #        print 'codigo no existe ', row
        data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'create', values)
