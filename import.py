#!/usr/bin/env python
import csv
import xmlrpclib

LOGFILE = 'import_log.csv'
SERVER = 'http://makeover.sytes.net:8069'
DATABASE = 'makeover'
USERNAME = 'admin'
PASSWORD = raw_input('Enter password: ')
CSVFILE = 'importacion-open.csv'
csv_default_code = 1
csv_list_price = 3

print "-------------------------------------"
print "updating database", DATABASE

# devuelve un writer para escribir un archivo csv sin quotas
def write_csv(filename):
    writer = csv.writer(open(filename, 'wb'), delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
    return writer


sock_common = xmlrpclib.ServerProxy(SERVER+'/xmlrpc/common')
uid = sock_common.login(DATABASE, USERNAME, PASSWORD)
sock = xmlrpclib.ServerProxy(SERVER+'/xmlrpc/object')

reader = csv.reader(open(CSVFILE,'rb'))
wr = write_csv(LOGFILE)

for row in reader:
    args = [('default_code','=',row[csv_default_code] )]
    ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', args)
    if len(ids) != 0:
        print row
        values = {'list_price': row[csv_list_price]}
        data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'write', ids, values)
    else:
        wr.writerow(row)



#fields = ['default_code','list_price','categ_id']
#data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', ids, fields)
#print(data)

