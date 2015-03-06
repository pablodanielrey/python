import psycopg2
import sys
import re
import uuid
import base64
import hashlib

user = sys.argv[1]
passw = sys.argv[2]
host = sys.argv[3]

user2 = sys.argv[4]
passw2 = sys.argv[5]


db = psycopg2.connect(host=host, user=user, password=passw, dbname="dcsys")
cursor = db.cursor()
cursor.execute('select username,student_number from students.users s, credentials.user_password p where s.id = p.user_id');
data = cursor.fetchall()
db.close()

db = psycopg2.connect(host=host, user=user2, password=passw2, dbname="au24")
cursor = db.cursor()
for d in data:
	print "modificando %s" % d[0]
	cursor.execute('update mdl_user set idnumber = %s where username = %s',(d[1],d[0]))
db.commit()
db.close()
