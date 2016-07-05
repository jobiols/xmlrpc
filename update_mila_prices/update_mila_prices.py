# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Script to check product prices
import csv

import odoorpc



# PASSWORD = raw_input('Enter password: ')
PASSWORD = 'melquiades'

data = {
    'server': 'http://localhost:8068',
    'database': 'makeover_datos',
    'username': 'admin',
    'password': PASSWORD,
}

csv_params = {
    'csvfile': 'mila-prices.csv',
    'category': 0,
    'default_code': 1,
    'name': 2,
    'list_price': 3,
    'sale_ok': 4,
    'purchase_ok': 5
}


class product:
    def __init__(self, line, parent):
        self._line = line
        self._parent = parent

    def _map_category(self, category):
        cat = {
            'MM': 25,
            'MP': 26,
            'M20A': 45,
            'P20A': 49
        }

        """
        25 Mila / Mila Marzi
        26 Mila / Mila Pro
        45 Mila / Mila Marzi / 20 Años
        49 Mila / Mila Pro / 20 Años
        """

        try:
            ret = cat[category]
        except:
            ret = 'titulo'
        return ret

    def _map_ok(self, ok):
        if ok == '1':
            return True
        else:
            return False

    def attr(self, name):
        if name == 'default_code':
            return self._line[self._parent._params[name]][1:-1]
        elif name == 'category':
            return self._map_category(self._line[self._parent._params[name]])
        elif name == 'sale_ok' or name == 'purchase_ok':
            return self._map_ok(self._line[self._parent._params[name]])
        else:
            return self._line[self._parent._params[name]].strip().replace('\n', ' ')


class csv_file:
    def __init__(self, params):
        self._params = params

    # devuelve un writer para escribir un archivo csv sin quotas
    def write_csv(self):
        writer = csv.writer(open(self._params['csvfile'], 'wb'), delimiter=',',
                            quotechar='',
                            quoting=csv.QUOTE_NONE)
        return writer

    # devuelve un reader para leer un archivo csv
    def _read_csv(self):
        return csv.reader(open(self._params['csvfile'], 'rb'))

    def obj(self):
        reader = self._read_csv()
        list = []
        for line in reader:
            if line[3] != 'pub':
                list.append(product(line, self))
        return list

# leer el archivo csv
file = csv_file(csv_params)

# conectar con odoo, proveer credenciales
odoo = odoorpc.ODOO('makeover.sytes.net', port=8068)
odoo.login('makeover_datos', 'admin', 'melquiades')

# obtener objeto category
# categ_obj = odoo.env['product.category']
# ids = categ_obj.search([])
# for cat in categ_obj.browse(ids):
#    print cat.id, cat.complete_name

# obtener objeto product
prod_obj = odoo.env['product.product']

# por cada linea del archivo mila hacer
for prod in file.obj():
    if False:
        print prod.attr('category')
        print prod.attr('default_code')
        print prod.attr('name')
        print prod.attr('list_price')
        print prod.attr('sale_ok')
        print prod.attr('purchase_ok')

    ids = prod_obj.search([('default_code', '=', prod.attr('default_code'))])
    recordset = prod_obj.browse(ids)


    # el producto ya existe en odoo
    if recordset:
        for rec in recordset:
            print 'Actua <<<<', prod.attr('default_code'), prod.attr('name')

            rec.write({'name': prod.attr('name'),
                       'categ_id': prod.attr('category'),
                       'list_price': prod.attr('list_price'),
                       'sale_ok': prod.attr('sale_ok'),
                       'purchase_ok': prod.attr('purchase_ok'),
                       'cost_method': 'real'
                       })

    # el producto no existe en odoo
    else:
        vals = {'name': prod.attr('name'),
                'default_code': prod.attr('default_code'),
                'categ_id': prod.attr('category'),
                'list_price': prod.attr('list_price'),
                'sale_ok': prod.attr('sale_ok'),
                'purchase_ok': prod.attr('purchase_ok'),
                'cost_method': 'real',
                'type': 'product'
                }
        print 'Crear >>>>', prod.attr('default_code'), prod.attr('name')
        prod_obj.create(vals)
