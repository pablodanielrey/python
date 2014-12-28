# -*- coding: utf-8 -*-
import json, uuid
import psycopg2
from model import Requests

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

  def handleAction(self, server, message):

    if message['action'] != 'aprobeRequest':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    pid = message['id']
    reqId = message['reqId']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      self.req.removeRequest(con,reqId)

      response = {'id':pid, 'ok':'request eliminado correctamente'}
      server.sendMessage(json.dumps(response))

    except psycopg2.DatabaseError, e:

        response = {'id':pid, 'error':''}
        server.sendMessage(json.dumps(response))

        print 'peticion error'

    finally:
        if con:
            con.close()

    return True
