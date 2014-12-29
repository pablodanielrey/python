
import uuid
import psycopg2
from model import ObjectView

class Users:

    def createUser(self,con,data):
        try:
            user = ObjectView.ObjectView(data)
            rreq = (str(uuid.uuid4()),user.dni,user.name,user.lastname)
            cur = con.cursor()
            cur.execute('insert into users (id,dni,name,lastname) values (%s,%s,%s,%s)', rreq)

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print e

    def listUsers(self, con):
        try:
            cur = con.cursor()
            cur.execute('select id,dni,name,lastname from users');
            data = cur.fetchall();

            ''' transformo a diccionario la respuesta '''
            rdata = []
            for d in data:
                rdata.append({
                    'id':d[0],
                    'dni':d[1],
                    'name':d[2],
                    'lastname':d[3]
                })

            return rdata

        except psycopg2.DatabaseError, e:
            print e
            return None
