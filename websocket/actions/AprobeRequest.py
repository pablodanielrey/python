# -*- coding: utf-8 -*-
import json, uuid
import psycopg2
from model import Requests
from model import Users
from model import ObjectView

"""
peticion:
{
  "id":"id de la peticion"
  "action":"aprobeRequest",
  "session":"id de session obtenido en el login",
  "reqId":"id de la peticion"
}

respuesta:
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

"""


class AprobeRequest:

  req = Requests.Requests()
  users = Users.Users()

  def handleAction(self, server, message):

    if message['action'] != 'aprobeRequest':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    pid = message['id']
    reqId = message['reqId']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      reqs = self.req.listRequests(con)
      for r in reqs:
          if r['id'] == reqId:
              r2 = ObjectView.ObjectView(r)
              user = { 'dni':r2.dni, 'name':r2.name, 'lastname':r2.lastname }
              self.users.createUser(con,user)
              self.req.removeRequest(con,reqId)
              con.commit()


      response = {'id':pid, 'ok':'usuario creado correctamente'}
      server.sendMessage(json.dumps(response))

    except psycopg2.DatabaseError, e:

        response = {'id':pid, 'error':''}
        server.sendMessage(json.dumps(response))

        if con:
            con.rollback()

    finally:
        if con:
            con.close()

    return True
