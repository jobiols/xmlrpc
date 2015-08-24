# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Script to increment product prices by percentage

import xmlrpclib

# categ to increment
CATEGORY = 'Lidherma'
INCREMENT = 1.12
DATE = '01/09/2015'

# SERVER = 'http://makeover.sytes.net:8069'
SERVER = 'http://makeover.sytes.net:8069'
DATABASE = 'makeover_datos'
USERNAME = 'admin'
PASSWORD = 'melquiades'
# raw_input('Enter password: ')

print "-------------------------------------"
print "updating database", DATABASE

sock_common = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/common')
uid = sock_common.login(DATABASE, USERNAME, PASSWORD)
sock = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/object')

# obtener los id de las categorias
ids = sock.execute(DATABASE, uid, PASSWORD, 'product.category', 'search', [])
fields = ['id', 'name']
categs = sock.execute(DATABASE, uid, PASSWORD, 'product.category', 'read', ids, fields)


def categ_to_id(categ):
    for cat in categs:
        if cat['name'] == categ:
            ret = cat['id']
            return ret
    return False

# buscar todos los idś de la categoria
args = [('categ_id', '=', categ_to_id(CATEGORY))]
ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', args)

# traer todos los precios
fields = ['list_price', 'description']
data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', ids, fields)

# por cada precio incrementarlo y volverlo a escribir
for prod in data:
    print prod
    if not prod['description']:
        prod['description'] = ''
    if prod['list_price'] != 1.0:
        values = {'list_price': prod['list_price'] * INCREMENT,
                  'description': prod[
                                     'description'] + '\n' + DATE+' aumento ' + str(
                      prod['list_price']) + ' + '+str((INCREMENT-1)*100)+'% ' + ' = ' + str(
                      prod['list_price'] * INCREMENT)
                  }
        print values
        data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'write',
                            prod['id'], values)
