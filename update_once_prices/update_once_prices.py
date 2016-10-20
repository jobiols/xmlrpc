# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Script to check product prices makeover

import odoorpc

PASSWORD = raw_input('Enter password: ')

login = {
    #    'server': '52.205.148.95',
    'server': 'localhost',
    'port': 8068,
    'database': 'makeover_datos',
    'username': 'admin',
    'password': PASSWORD,
}

# conectar con odoo, proveer credenciales
odoo = odoorpc.ODOO(login.get('server'), port=login.get('port'))
odoo.login(login.get('database'), login.get('username'), login.get('password'))

prod_cat = odoo.env['product.category']
categ_id = prod_cat.search([('name', '=', 'Farmacia Once')])[0]

prod = odoo.env['product.product']
ids = prod.search([('categ_id', '=', categ_id)])
print ids

for pro in prod.browse(ids):
    print pro.name
