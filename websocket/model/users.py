# -*- coding: utf-8 -*-
import uuid
import psycopg2
from model.objectView import ObjectView

class Users:

    def createMail(self,con,data):
        try:
            mail = ObjectView(data)
            rreq = (str(uuid.uuid4()),mail.user_id,mail.email,False)
            cur = con.cursor()
            cur.execute('insert into user_mails (id,user_id,email,confirmed) values (%s,%s,%s,%s)', rreq)

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e


    def findMail(self,con,id):
        try:
            cur = con.cursor()
            cur.execute('select id,user_id,email,confirmed from user_mails where id = %s', (id,))
            data = cur.fetchone()
            if data != None:
                return self.convertMailToDict(data)
            else:
                return None

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e



    def listMails(self, con, user_id):
        try:
            cur = con.cursor()
            cur.execute('select id, user_id, email, confirmed from user_mails where user_id = %s',(user_id,))
            data = cur.fetchall()
            rdata = []
            for d in data:
                rdata.append(self.convertMailToDict(d))
            return rdata

        except psycopg2.DatabaseError, e:
            print e
            return None


    def deleteMail(self,con,id):
        try:
            cur = con.cursor()
            cur.execute('delete from user_mails where id = %s', (id,))

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e



    def updateMail(self,con,data):
        try:
            mail = ObjectView(data)
            rreq = (mail.email, mail.confirmed, mail.id)
            cur = con.cursor()
            cur.execute('update user_mails set email = %s, confirmed = %s where id = %s', rreq)

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e


    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertMailToDict(self,d):
        rdata = {
                'id':d[0],
                'user_id':d[1],
                'email':d[2],
                'confirmed':d[3]
            }
        return rdata


    """-------------------------------"""

    def createUser(self,con,data):
        try:
            user = ObjectView(data)
            rreq = (str(uuid.uuid4()),user.dni,user.name,user.lastname)
            cur = con.cursor()
            cur.execute('insert into users (id,dni,name,lastname) values (%s,%s,%s,%s)', rreq)

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e

    def updateUser(self,con,data):
        try:
            user = ObjectView(data)
            rreq = (user.dni,user.name,user.lastname, user.id)
            cur = con.cursor()
            cur.execute('update users set dni = %s, name = %s, lastname = %s where id = %s', rreq)

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e


    def findUser(self,con,id):
        try:
            cur = con.cursor()
            cur.execute('select id,dni,name,lastname from users where id = %s', (id,))
            data = cur.fetchone()
            if data != None:
                return self.convertUserToDict(data)
            else:
                return None

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e


    def listUsers(self, con):
        try:
            cur = con.cursor()
            cur.execute('select id,dni,name,lastname from users')
            data = cur.fetchall()
            rdata = []
            for d in data:
                rdata.append(self.convertUserToDict(d))
            return rdata

        except psycopg2.DatabaseError, e:
            print e
            return None


    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertUserToDict(self,d):
        rdata = {
                'id':d[0],
                'dni':d[1],
                'name':d[2],
                'lastname':d[3]
            }
        return rdata
