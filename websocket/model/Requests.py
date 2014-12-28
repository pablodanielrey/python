# -*- coding: utf-8 -*-
import psycopg2

class Requests:

    def listRequests(self, con):
        try:
            cur = con.cursor()
            cur.execute('select id,dni,name,lastname,email,reason from account_requests');
            data = cur.fetchall();

            ''' transformo a diccionario la respuesta '''
            rdata = []
            for d in data:
                rdata.append({
                    'id':d[0],
                    'dni':d[1],
                    'name':d[2],
                    'lastname':d[3],
                    'email':d[4],
                    'reason':d[5]
                })

            return rdata

        except psycopg2.DatabaseError, e:
            print e
            return None


    def createRequest(self, con, req):
        try:
            rreq = (req['id'],req['dni'],req['name'],req['lastname'],req['email'],req['reason'])
            cur = con.cursor()
            cur.execute('insert into account_requests (id,dni,name,lastname,email,reason) values (%s,%s,%s,%s,%s,%s)', rreq)
            con.commit()

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e


    def removeRequest(self, con, rid):
        try:
            cur = con.cursor()
            cur.execute('delete from account_requests where id = %s', (rid,))
            con.commit()

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e

        except TypeError, e:
            print e

        except Error, e:
            print e
