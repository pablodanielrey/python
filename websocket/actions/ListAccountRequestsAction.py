# -*- coding: utf-8 -*-
import json, uuid
import psycopg2
from model import Requests

"""
peticion:
{
    "id":"",
    "action":"listAccountRequests"
    "session":"sesion de usuario"
}

respuesta:
{
    "id":"id de la petición",
    "requests":[
        {
         "id":"",
         "dni":"",
         "name":"",
         "lastname":"",
         "email":""
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListAccountRequestsAction:

  req = Requests.Requests()

  def handleAction(self, server, message):

    if message['action'] != 'listAccountRequests':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      rdata = self.req.listRequests(con)
      response = {'id':message['id'], 'ok':'', 'requests': rdata}
      print json.dumps(response);
      server.sendMessage(json.dumps(response))

    except psycopg2.DatabaseError, e:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(json.dumps(response))

    finally:
        if con:
            con.close()

    return True
