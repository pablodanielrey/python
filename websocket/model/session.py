# -*- coding: utf-8 -*-
import uuid

"""
datos de la entidad:

{
    id:'id de la sesion',
    data:'datos variables de sesion'
}

"""


class Session:

    sessions = []

    def create(self,data):
        id = str(uuid.uuid4());
        self.sessions.append({'id':id,'data':data});
        return id

    def destroy(self, id):
        for s in self.sessions:
            if s['id'] == id:
                self.sessions.remove(s)
                return
