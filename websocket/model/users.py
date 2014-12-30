# -*- coding: utf-8 -*-
import uuid
import psycopg2
from model.objectView import ObjectView

class Users:

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
            cur.execute('update users set (dni = %s, name = %s, lastname = %s) where id = %s', rreq)

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
                return self.convertToDict(data)
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
                rdata.append(self.convertToDict(d))
            return rdata

        except psycopg2.DatabaseError, e:
            print e
            return None


    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertToDict(self,d):
        rdata = {
                'id':d[0],
                'dni':d[1],
                'name':d[2],
                'lastname':d[3]
            }
        return rdata
