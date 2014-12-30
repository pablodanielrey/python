# -*- coding: utf-8 -*-
import uuid
import psycopg2
from model.objectView import ObjectView

"""

datos de la entidad

{
    username:''
    password:''
    user_id:''
    id:''
}

"""

class UserPassword:

    def createUserPassword(self,con,data):
        try:
            user = ObjectView(data)
            rreq = (str(uuid.uuid4()),user.user_id,user.username,user.password)
            cur = con.cursor()
            cur.execute('insert into user_password (id,user_id,username,password) values (%s,%s,%s,%s)', rreq)

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e


    def updateUserPassword(self,con,data):
        try:
            user = ObjectView(data)
            rreq = (user.user_id, user.username, user.password, user.id)
            cur = con.cursor()
            cur.execute('update users set (user_id = %s, username = %s, password = %s) where id = %s', rreq)

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e


    def findUserPassword(self,con,credentials):
        try:
            cred = ObjectView(credentials)
            cur = con.cursor()
            cur.execute('select id, user_id from user_password where username = %s and password = %s', (cred.username,cred.password))
            data = cur.fetchone()
            if data != None:
                return self.convertToDict(data)
            else:
                return None

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e


    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertToDict(self,d):
        rdata = {
                'id':d[0],
                'user_id':d[1]
            }
        return rdata
