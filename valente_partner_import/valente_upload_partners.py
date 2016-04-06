# -*- coding: utf-8 -*-
# ################################################################################
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
# ################################################################################
import csv
import xmlrpclib

from  server_data import DATABASE, SERVER, USERNAME, PASSWORD



# donde están los datos
CSVFILE = 'datos_partners_valente.csv'
csv_default_code = 0

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

exit(0)

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


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
