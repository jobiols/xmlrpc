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
csv_nombre = 1
csv_direccion = 2
csv_telef1 = 3
csv_telef2 = 4
csv_cp = 5
csv_IVA = 6
csv_cuit = 7
csv_cliente = 9
csv_proveedor = 10

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

# buscar todos los idś
args = ['|', ('supplier', '=', True), ('customer', '=', True)]
ids = sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'search', args)

print 'borrar todo'
# borrar todo
sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'unlink', ids, {})
print 'todo borrado'


# traer todos los partners
# data = sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'read', ids, fields)
# ids = sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'search', args)

def doc_type(resp):
    if resp == '1': return 6
    if resp == '2': return 1
    if resp == '3': return 3
    if resp == '4': return 4
    if resp == '5': return 5
    if resp == '6': return 7


errors = 0
duplicates = 0
# recorrer todo el archivo
for rec in reader:
    # el primer registro tiene nombre en el nombre, no lo proceso.
    if rec[csv_nombre] != 'nombre':
        # sacarle los guiones al cuit
        cuit = rec[csv_cuit][0:2] + rec[csv_cuit][3:11] + rec[csv_cuit][12:]
        if cuit == '0':
            cuit = ''

        # buscar si existe el cuit
        args = [('document_number', '=', cuit)]
        ids = sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'search', args)

        fields = ['name', 'document_number']
        data = sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'read', ids, fields)
        # si no existe en la bd y no es cero, por
        if not ids:
            # add register
            if len(cuit) != 11:
                document_type = ''
            else:
                document_type = 25

            values = {}
            values['name'] = rec[csv_nombre]
            values['street'] = rec[csv_direccion]
            values['phone'] = rec[csv_telef1]
            values['fax'] = rec[csv_telef2]
            values['zip'] = rec[csv_cp]
            values['responsability_id'] = doc_type(rec[csv_IVA])
            if len(cuit) == 11:
                values['document_number'] = cuit
                values['vat'] = 'AR' + cuit
                values['document_type_id'] = document_type
            values['supplier'] = rec[csv_proveedor] == '1'
            values['customer'] = rec[csv_cliente] == '1'
            values['country_id'] = 11
            try:
                data = sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'create',
                                    values)
            except:
                print 'error', cuit
                errors += 1
        else:
            print values
            duplicates += 1

print 'errores', errors
print 'duplicados', duplicates
