#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script para eliminar las cuentas de impuestos de los productos
# No se pueden eliminar por aca, porque son tablas relacionales las eliminé x sql
#
import xmlrpclib

print "Se van a eliminar los impuesto de todos los productos"
from  server_access.server_data import DATABASE, SERVER, USERNAME, PASSWORD

print "Delete product taxes -------------------------"
print "updating database", DATABASE, ' on server', SERVER

sock_common = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/common')
uid = sock_common.login(DATABASE, USERNAME, PASSWORD)
sock = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/object')

# obtener todos los id de los productos
args = [('default_code', '=', '1000-01')]
ids = sock.execute(DATABASE, uid, PASSWORD, 'product.template', 'search', args)
print 'corrigiendo ', len(ids), ' productos...'

args = [('default_code', '=', '1000-01')]
ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', args)
fields = ['default_code', 'taxes_id', 'supplier_taxes_id', 'lst_price']
data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', ids, fields)
for d in data:
    print(d)






# poner las cuentas de impuestos en ''
values = {'taxes_id': '123', 'supplier_taxes_id': 'adsf', 'lst_price': 200}
j = len(ids)
for id in ids:
    print "restan ", j
    j -= 1
    data = sock.execute(DATABASE, uid, PASSWORD, 'product.template', 'write', id, values)
    print "resultado ", data
