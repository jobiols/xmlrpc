#!/usr/bin/env python
import csv
import xmlrpclib
from  server_access.server_data import DATABASE, SERVER, USERNAME, PASSWORD

LOGFILE = 'import_log.csv'
CSVFILE = 'product_prices.csv'
csv_default_code = 1
csv_list_price = 3

# devuelve un writer para escribir un archivo csv sin quotas
def write_csv(filename):
    writer = csv.writer(open(filename, 'wb'), delimiter=',', quotechar='',
                        quoting=csv.QUOTE_NONE)
    return writer


sock_common = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/common')
uid = sock_common.login(DATABASE, USERNAME, PASSWORD)
sock = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/object')

reader = csv.reader(open(CSVFILE, 'rb'))
wr = write_csv(LOGFILE)
# categ 25 26
# recorrer todos los registros de la bd
# args = [('state','=','obsolete'),('state','=','end')]
args = [('categ_id', '=', 25)]
ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', args)

print len(ids)
fields = ['default_code', 'list_price', 'state', 'product_tmpl_id', 'categ_id']
data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', ids, fields)
print data


# args = [('state','=',row[csv_default_code] )]

# ids = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'search', args)
# if len(ids) != 0:
#    fields = ['default_code','list_price','state','product_tmpl_id']
#    data = sock.execute(DATABASE, uid, PASSWORD, 'product.product', 'read', ids, fields)
#    print data

# else:
#    wr.writerow(row)
