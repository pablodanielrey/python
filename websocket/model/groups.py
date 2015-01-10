# -*- coding: utf-8 -*-

class Groups:


    def listGroups(self, con):
        cur = con.cursor()
        cur.execute('select id,system_id,name from groups')
        data = cur.fetchall()
        rdata = []
        for d in data:
            rdata.append(self.convertToDict(d))
        return rdata


    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertToDict(self,d):
        rdata = {
                'id':d[0],
                'system_id':d[1],
                'name':d[2]
            }
        return rdata
