# -*- coding: utf-8 -*-

import csv
import uuid
import sys
import psycopg2

host = sys.argv[1]
user = sys.argv[2]
passw = sys.argv[3]

db = psycopg2.connect(host=host, user=user, password=passw, dbname="dcsys")
cursor = db.cursor()

csvr = csv.reader(sys.stdin,delimiter=',')
for name,dni,mail in csvr:
    cursor.execute('select id from profile.users where dni = %s',(dni,))
    user = cursor.fetchone()
    if user == None:
        print('%s no existe', dni)
        continue
    userId = user[0]
    cursor.execute('insert into credentials.auth_profile (user_id,profile) values (%s,%s)',(userId,'USER-TUTOR'))

db.commit()
db.close()
