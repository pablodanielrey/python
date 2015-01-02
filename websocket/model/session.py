# -*- coding: utf-8 -*-
import uuid
import time
import inject

"""
datos de la entidad:

{
    id:'id de la sesion',
    data:'datos variables de sesion'
}

"""

class SessionNotFound(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return 'Sesion no encontrada'

class SessionExpired(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return 'Sesion expirada'


class Session:

    expire = int(60 * 60)
    sessions = []


    def __str__(self):
        sr = ''
        for s in self.sessions:
            sr = sr + str(s) + '\n'
        return sr

    def findSession(self,id):
        for s in self.sessions:
            if (s['id'] == id):
                return s
        raise SessionNotFound()


    def checkTime(self,s,t):
        return (s['expire'] <= t)

    def removeExpired(self):
        expire = time.time()
        for s in self.sessions:
            if self.checkTime(s,expire):
                print 'Expirando session : ' + str(s)
                self.sessions.remove(s)



    def create(self,data):
        self.removeExpired()
        id = str(uuid.uuid4());
        actual = time.time()
        expire = actual + self.expire
        self.sessions.append({
            'id':id,
            'data':data,
            'expire':expire
        });
        return id

    def destroy(self, id):
        s = self.findSession(id)
        self.sessions.remove(s)
        self.removeExpired()

    def getSession(self,id):
        s = self.findSession(id)
        expire = time.time()
        if self.checkTime(s,expire):
            raise SessionExpired()
        self.removeExpired()
        return s['data']
