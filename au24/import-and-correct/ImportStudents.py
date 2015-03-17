# -*- coding: utf-8 -*-

import csv
import ldap
import ldap.modlist as modlist
import uuid
import sys
import psycopg2

host = sys.argv[1]
user = sys.argv[2]
passw = sys.argv[3]

db = psycopg2.connect(host=host, user=user, password=passw, dbname="dcsys")

cursor = db.cursor()
cursor.execute('select pu.id,dni,name,lastname,student_number from profile.users pu left join students.users s on s.id = pu.id')
alldata = cursor.fetchall()

bydni = {}
bysn = {}

for data in alldata:
    uid,dni,name,lastname,student_number = data
    bydni[dni] = data
    if student_number != None:
        bysn[student_number] = data


reader = csv.reader(sys.stdin, delimiter=',')
for apellido,nombre,legajo,dni,nada in reader:
    #print "Nombre : ", nombre
    #print "Apellido :", apellido
    #print "Legajo : ", legajo
    #print "Dni : ", dni

    if dni in bydni:
        """ actualizo la persona """
        uid, dni, name, lastname, student_number = bydni[dni]

        """ controlo que el legajo asignado sea el de la persona """
        if legajo in bysn:
            uid2, dni2, name2, lastname2, student_number2 = bysn[legajo]
            if uid2 != uid:
                print "el legajo %s asignado al dni %s ya está asignado" % (legajo,dni2)
            else:
                cursor.execute('update students.users set student_number = %s where id = %s', (legajo,uid))
                if cursor.rowcount <= 0:
                    cursor.execute('insert into students.users (id,student_number,condition) values (%s,%s,%s)',(uid,legajo,'regular'))

        cursor.execute('update au24.users set type = %s where id = %s', ('ingresante',uid))
        if cursor.rowcount <= 0:
            cursor.execute('insert into au24.users (id,type) values (%s,%s)',(uid,'ingresante'))

        cursor.execute('update profile.users set name = %s, lastname = %s where id = %s', (nombre,apellido,uid))
        db.commit()

    else:

        if legajo in bysn:
            print "dni %s no existente, pero legajo %s ya existe" % (dni,legajo)
            continue

        """ creo la persona """
        print "creando " + dni
        uid = str(uuid.uuid4())
        cursor.execute('insert into profile.users (id,name,lastname) values (%s,%s,%s)', (uid,nombre,apellido))
        cid = str(uuid.uuid4())
        cursor.execute('insert into credentials.user_password (id,user_id,username,password) values (%s,%s,%s,%s)', (cid,uid,dni,dni[-4:]))

        cursor.execute('update students.users set student_number = %s where id = %s', (legajo,uid))
        if cursor.rowcount <= 0:
            cursor.execute('insert into students.users (id,student_number,condition) values (%s,%s,%s)',(uid,legajo,'regular'))

        cursor.execute('update au24.users set type = %s where id = %s', ('ingresante',uid))
        if cursor.rowcount <= 0:
            cursor.execute('insert into au24.users (id,type) values (%s,%s)',(uid,'ingresante'))

        db.commit()

db.close()
