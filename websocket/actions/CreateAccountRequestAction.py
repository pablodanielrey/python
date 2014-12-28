# -*- coding: utf-8 -*-
import json, uuid
import ActionUtils
import psycopg2


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
    "mail":""
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

  createRequest = 'insert into account_requests (dni,name,lastname,email,reason) values (%s,%s,%s,%s,%s)'

  def handleAction(self, server, message):

    if message['action'] != 'createAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    pid = message['id']

    dni = message['request']['dni']
    name = message['request']['name']
    lastname = message['request']['lastname']
    mail = message['request']['email']
    reason = message['request']["reason"]

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      cur = con.cursor()
      cur.execute(self.createRequest,(dni,name,lastname,mail,reason))
      con.commit()

      response = {'id':pid, 'ok':'petición creada correctamente'}
      server.sendMessage(json.dumps(response))

      print 'peticion creada correctamente'

    except psycopg2.DatabaseError, e:

        if con:
            con.rollback()

        response = {'id':pid, 'error':''}
        server.sendMessage(json.dumps(response))

        print 'peticion error'

    finally:
        if con:
            con.close()

    return True
