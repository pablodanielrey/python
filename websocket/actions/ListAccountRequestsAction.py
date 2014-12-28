# -*- coding: utf-8 -*-
import json, uuid
import psycopg2

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

  query = 'select id,dni,name,lastname,email,reason from account_requests';

  def handleAction(self, server, message):

    if message['action'] != 'listAccountRequests':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      cur = con.cursor()
      cur.execute(self.query);
      data = cur.fetchall();

      ''' transformo a diccionario la respuesta '''
      rdata = []
      for d in data:
          rdata.append({
            'id':d[0],
            'dni':d[1],
            'name':d[2],
            'lastname':d[3],
            'email':d[4],
            'reason':d[5]
           })

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
