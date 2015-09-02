#!/usr/bin/env python
# Script para importar las clases desde el drive
#
import csv
import xmlrpclib
from datetime import datetime
from  server_access.server_data import DATABASE, SERVER, USERNAME, PASSWORD


LOGFILE = 'import_lectures_log.csv'
CSVFILE = 'Cursos - Programacion.csv'

csv_publicar = 0
csv_clase = 1
csv_curso = 2
csv_inicio = 3
csv_descripcion_curso = 4
csv_descripcion_de_clase = 5
csv_fecha = 6
csv_dia = 7
csv_horario = 8
csv_dura = 9
csv_desde = 10
csv_hasta = 11

print "-------------------------------------"
print "updating database", DATABASE

# devuelve un writer para escribir un archivo csv sin quotas
def write_csv(filename):
    writer = csv.writer(open(filename, 'wb'), delimiter=',', quotechar='',
                        quoting=csv.QUOTE_NONE)
    return writer


def get_instance(row):
    curso = row[csv_curso]
    try:
        i = int(curso[-2:])
    except:
        i = 0
    return i


def get_date(row):
    try:
        date = datetime.strftime(datetime.strptime(row[csv_fecha], "%d/%m/%Y"),
                                 "%Y-%m-%d")
    except:
        print "revento get_date"
    return date


def get_default_code(curso):
    curso = row[csv_curso]
    return curso[:-2]


sock_common = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/common')
uid = sock_common.login(DATABASE, USERNAME, PASSWORD)
sock = xmlrpclib.ServerProxy(SERVER + '/xmlrpc/object')

reader = csv.reader(open(CSVFILE, 'rb'))
wr = write_csv(LOGFILE)

# Borrar todas las clases
ids = sock.execute(DATABASE, uid, PASSWORD, 'curso.lecture', 'search', [])
sock.execute(DATABASE, uid, PASSWORD, 'curso.lecture', 'unlink', ids, {})

for row in reader:
    #   obtener la instancia para buscar el curso
    args = [('instance', '=', get_instance(row)),
            ('default_code', '=', get_default_code(row))]
    ids = sock.execute(DATABASE, uid, PASSWORD, 'curso.curso', 'search', args)
    fields = ['id', 'schedule_1']

    #   leer el curso correspondiente
    data = sock.execute(DATABASE, uid, PASSWORD, 'curso.curso', 'read', ids, fields)
    if len(ids) != 0:
        for value in data:
            #           Si no tiene horario no le cargo las clases
            if value['schedule_1']:
                values = {
                    'date': get_date(row),
                    'desc': row[csv_descripcion_de_clase],
                    'curso_id': value['id'],
                    'schedule_id': value['schedule_1'][0]
                }
                print values
                data = sock.execute(DATABASE, uid, PASSWORD, 'curso.lecture', 'create',
                                    values)
    else:
        #       el curso no existe
        print("el curso ", args, " no existe")
        raise ("el curso ", args, " no existe")
