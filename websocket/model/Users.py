
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
