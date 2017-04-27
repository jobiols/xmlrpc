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
# -*- coding: utf-8 -*-
# !/usr/bin/env pythonme

import odoorpc

PASSWORD = raw_input('Validate Groupon: ')

login = {
    'server': 'localhost',
    'port': 8068,
    'database': 'makeover_datos',
    'username': 'admin',
    'password': PASSWORD,
}

# conectar con odoo, proveer credenciales
odoo = odoorpc.ODOO(login.get('server'), port=login.get('port'))
odoo.login(login.get('database'), login.get('username'), login.get('password'))
print 'conectado'

# obtener objeto partner
prod_obj = odoo.env['res.partner']
ids = prod_obj.search([('function', '!=', False),
                       ('groupon', '=', False)])
for prod in prod_obj.browse(ids):
    #chequear que la longitud del groupon sea 10, sinó es otra cosa que escribieron ahi.
    if len(prod.function) == 10:
        print prod.function, prod.name
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
