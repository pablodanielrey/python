# -*- coding: utf-8 -*-
import uuid
import psycopg2
from model.objectView import ObjectView

class Users:


    def createMail(self,con,data):
        mail = ObjectView(data)
        mid = str(uuid.uuid4())
        rreq = (mid,mail.user_id,mail.email,False,'')
        cur = con.cursor()
        cur.execute('insert into user_mails (id,user_id,email,confirmed,hash) values (%s,%s,%s,%s,%s)', rreq)
        return mid

    def findMailByHash(self,con,hash):
        cur = con.cursor()
        cur.execute('select id,user_id,email,confirmed,hash from user_mails where hash = %s', (hash,))
        data = cur.fetchone()
        if data != None:
            return self.convertMailToDict(data)
        else:
            return None

    def findMail(self,con,id):
        cur = con.cursor()
        cur.execute('select id,user_id,email,confirmed,hash from user_mails where id = %s', (id,))
        data = cur.fetchone()
        if data != None:
            return self.convertMailToDict(data)
        else:
            return None

    def listMails(self, con, user_id):
        cur = con.cursor()
        cur.execute('select id, user_id, email, confirmed, hash from user_mails where user_id = %s',(user_id,))
        data = cur.fetchall()
        rdata = []
        for d in data:
            rdata.append(self.convertMailToDict(d))
        return rdata

    def deleteMail(self,con,id):
        cur = con.cursor()
        cur.execute('delete from user_mails where id = %s', (id,))


    def updateMail(self,con,data):
        if 'hash' not in data:
            data['hash'] = ''
        mail = ObjectView(data)
        rreq = (mail.email, mail.confirmed, mail.hash, mail.id)
        cur = con.cursor()
        cur.execute('update user_mails set email = %s, confirmed = %s, hash = %s where id = %s', rreq)


    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertMailToDict(self,d):
        rdata = {
                'id':d[0],
                'user_id':d[1],
                'email':d[2],
                'confirmed':d[3],
                'hash':d[4]
            }
        return rdata


    """-------------------------------"""

    def createUser(self,con,data):
        user = ObjectView(data)
        uid = str(uuid.uuid4())
        rreq = (uid,user.dni,user.name,user.lastname)
        cur = con.cursor()
        cur.execute('insert into users (id,dni,name,lastname) values (%s,%s,%s,%s)', rreq)
        return uid

    def updateUser(self,con,data):
        user = ObjectView(data)
        rreq = (user.dni,user.name,user.lastname, user.id)
        cur = con.cursor()
        cur.execute('update users set dni = %s, name = %s, lastname = %s where id = %s', rreq)
        if cur.rowcount <= 0:
            raise Exception()


    def findUserByDni(self,con,dni):
        cur = con.cursor()
        cur.execute('select id,dni,name,lastname from users where dni = %s', (dni,))
        data = cur.fetchone()
        if data != None:
            return self.convertUserToDict(data)
        else:
            return None

    def findUser(self,con,id):
        cur = con.cursor()
        cur.execute('select id,dni,name,lastname from users where id = %s', (id,))
        data = cur.fetchone()
        if data != None:
            return self.convertUserToDict(data)
        else:
            return None

    def listUsers(self, con):
        cur = con.cursor()
        cur.execute('select id,dni,name,lastname from users')
        data = cur.fetchall()
        rdata = []
        for d in data:
            rdata.append(self.convertUserToDict(d))
        return rdata


    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertUserToDict(self,d):
        rdata = {
                'id':d[0],
                'dni':d[1],
                'name':d[2],
                'lastname':d[3]
            }
        return rdata
