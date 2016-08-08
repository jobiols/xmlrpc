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
import xmlrpclib

SERVER = 'http://localhost:8068'
# SERVER = 'http://localhost:8068'
DATABASE = 'makeover_test'
USERNAME = 'admin'
print 'conectando con ',SERVER
PASSWORD = raw_input('Enter password: ')

print "-------------------------------------"
print "touching database", DATABASE

sock_common = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/common')
uid = sock_common.login(DATABASE, USERNAME, PASSWORD)
sock = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/object')

# buscar todos los idś de partners con date
args = [('date', '!=', False)]
ids = sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'search', args)

print 'tocando...{} registros '.format(len(ids))
# recorrer todo el archivo

fields = ['name', 'date']
for id in ids:
    data = sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'read', [id], fields)
    print '>>>', data
    values = {'date': data[0]['date']}
    print values
    sock.execute(DATABASE, uid, PASSWORD, 'res.partner', 'write', id, values)
    print data

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
