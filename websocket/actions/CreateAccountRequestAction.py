# -*- coding: utf-8 -*-
import json, uuid
import psycopg2
from model import Requests

"""
peticion:
{
  "id":"id de la peticion"
  "action":"createAccountRequest",
  "session":"id de session obtenido en el login"

  "request":{
    "dni":""
    "name":""
    "lastname":""
    "email":""
    "reason":""
  }
}

respuesta:
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

"""


class CreateAccountRequestAction:

  req = Requests.Requests()

  def handleAction(self, server, message):

    if message['action'] != 'createAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    pid = message['id']

    data = message['request']
    data['id'] = str(uuid.uuid4());

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      self.req.createRequest(con,data)
      con.commit()

      response = {'id':pid, 'ok':'petición creada correctamente'}
      server.sendMessage(json.dumps(response))

    except psycopg2.DatabaseError, e:

        response = {'id':pid, 'error':''}
        server.sendMessage(json.dumps(response))

        print 'peticion error'

    finally:
        if con:
            con.close()

    return True
