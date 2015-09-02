#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script para eliminar las cuentas de impuestos de los productos
#
import xmlrpclib
from  server_access.server_data import DATABASE, SERVER, USERNAME, PASSWORD

print "----------------------------------------"
print "updating database", DATABASE, ' on server', SERVER

sock_common = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/common')
uid = sock_common.login(DATABASE, USERNAME, PASSWORD)
sock = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/object')

# obtener todos los id de los productos
ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', [])
print 'corrigiendo ', len(ids), ' productos...'

# poner las cuentas de impuestos en ''
values = {'property_account_income': '', 'property_account_expense': ''}
for id in ids:
    data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'write', id, values)
