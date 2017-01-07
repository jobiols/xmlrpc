# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------------
import csv

import odoorpc


# PASSWORD = raw_input('Enter password: ')
PASSWORD = 'admin17'

login = {
    'server': 'localhost',
    'port': 8069,
    'database': 'reves_prod',
    'username': 'admin',
    'password': PASSWORD,
}

csv_stock = {
    'csvfile': 'products.csv',
    'location': 0,
    'default_code': 1,
    'qty': 2
}


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
            dict = {}
            dict['location'] = line[0]
            dict['default_code'] = line[1]
            dict['qty'] = line[2]
            list.append(dict)
        list.pop(0)
        return list

# conectar con odoo, proveer credenciales
odoo = odoorpc.ODOO(login.get('server'), port=login.get('port'))
odoo.login(login.get('database'), login.get('username'), login.get('password'))

stock = csv_file(csv_stock)
prod_obj = odoo.env['product.product']
inventory_obj = odoo.env['stock.inventory']
inventory_line_obj = odoo.env['stock.inventory.line']
product_obj = odoo.env['product.product']
warehouse_obj = odoo.env['stock.location']


# obtener el id de cada warehouse
for wh_id in warehouse_obj.search([('usage', '=', 'internal')]):
    wh = warehouse_obj.browse(wh_id)
    print wh.location_id.name

    # Crear un inventario en borrador
    ids = inventory_obj.create({'name': 'INV ' + wh.location_id.name,
                                'location_id': wh.id})
    inventory_id = inventory_obj.browse(ids)

    # Buscat todos los productos que van en ese almacen
    for data in stock.obj():
        if data['location'] == wh.location_id.name:
            print data['location'], data['default_code'], data['qty']
            # buscar id del producto
            ids = prod_obj.search([('default_code', '=', data['default_code'])])
            prod = prod_obj.browse(ids)

            # insertar en inventario
            line_data = {
                'inventory_id': inventory_id.id,
                'product_qty': data['qty'],
                'location_id': wh.id,
                'product_id': prod.id,
                'product_uom_id': prod.uom_id.id,
                'theoretical_qty': 0,
            }
            inventory_line_obj.create(line_data)
