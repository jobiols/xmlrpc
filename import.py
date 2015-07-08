#!/usr/bin/env python

import csv
from xmlrpclib import ServerProxy

SERVER = 'http://localhost:8069'
DATABASE = 'testcompany'
USERNAME = 'admin'
PASSWORD = 'password'

FILE_PATH = 'ODOO_clientsMain2_test.csv'

server = ServerProxy('http://localhost:8069/xmlrpc/common')
user_id = server.login(DATABASE, USERNAME, PASSWORD)

server = ServerProxy('http://localhost:8069/xmlrpc/object')

def search(list, key):
    for item in list:
        return item[key]

reader = csv.reader(open(FILE_PATH,'rb'))

for row in reader:
    #print row
    partner_template = {
        'name': row[0],
        #'company_id': row[1],
    }
    if row[2] is not None and row[2]<>'':
        partner_template.update({'email': row[2]})
    if row[5] is not None and row[5]<>'':
        partner_template.update({'tin': row[5]})
    if row[6] is not None and row[6]<>'':
        partner_template.update({'ref': row[6]})
    if row[8] is not None and row[8]<>'':
        partner_template.update({'phone': row[8]})
    if row[9] is not None and row[9]<>'':
        partner_template.update({'mobile': row[9]})

    print partner_template

    partner_id = server.execute_kw(DATABASE, user_id, PASSWORD, 'res.partner', 'create', [partner_template])

    #create External ID
    
    external_ids = {
       'model': 'res.partner',
       'name': row[11],
       'res_id': partner_id,
    }
    external_id = server.execute_kw(DATABASE, user_id, PASSWORD, 'ir.model.data', 'create', [external_ids])

    # update related fields

    if row[7] is not None and row[7]<>'':
        #look up and update payment term

        payment_term_id = server.execute_kw(DATABASE, user_id, PASSWORD, 'account.payment.term', 'search_read', [[['name','=',row[7]],['active', '=', True]]],{'fields': ['id'], 'limit': 1})
        if payment_term_id is not None:
            id = server.execute_kw(DATABASE, user_id, PASSWORD, 'res.partner', 'write', [[partner_id],{'property_payment_term': search(payment_term_id,'id')}])

    if row[10] is not None and row[10]<>'':
        #look up and update pricelist

        pricelist_id = server.execute_kw(DATABASE, user_id, PASSWORD, 'product.pricelist', 'search_read', [[['name','=',row[10]],['active', '=', True]]],{'fields': ['id'], 'limit': 1})

        if pricelist_id is not None:
            id = server.execute_kw(DATABASE, user_id, PASSWORD, 'res.partner', 'write', [[partner_id],{'property_product_pricelist': search(pricelist_id,'id')}])
