# -*- coding: utf-8 -*-

class Groups:

    def findMembers(self,con,id):
        cur = con.cursor()
        cur.execute('select user_id from groups_users where group_id = %s',(id,))
        data = cur.fetchall()
        rdata = []
        for d in data:
            rdata.append(d[0])
        return rdata


    def findGroup(self,con,id):
        cur = con.cursor()
        cur.execute('select id,system_id,name from groups where id = %s',(id,))
        g = cur.fetchone()
        group = self.convertToDict(g)
        return group


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
                'systemId':d[1],
                'name':d[2]
            }
        return rdata
