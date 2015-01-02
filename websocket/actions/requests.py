# -*- coding: utf-8 -*-
import json, uuid, psycopg2, inject
from model.requests import Requests
from model.users import Users
from model.objectView import ObjectView
from model.events import Events
from model.profiles import Profiles


"""
    Modulo de acceso a la capa de las peticiones de cuentas.

"""


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


class CreateAccountRequest:

  req = inject.attr(Requests)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)

  def handleAction(self, server, message):

    if message['action'] != 'createAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])


    pid = message['id']

    data = message['request']
    data['id'] = str(uuid.uuid4());

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      self.req.createRequest(con,data)
      con.commit()

      response = {'id':pid, 'ok':'petición creada correctamente'}
      server.sendMessage(json.dumps(response))

      event = {
        'type':'NewAccountRequestEvent',
        'data':data['id']
      }
      self.events.broadcast(server,event)


    except psycopg2.DatabaseError, e:

        response = {'id':pid, 'error':''}
        server.sendMessage(json.dumps(response))

        print 'peticion error'

    finally:
        if con:
            con.close()

    return True





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

class ListAccountRequests:

  req = Requests()

  def handleAction(self, server, message):

    if message['action'] != 'listAccountRequests':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])


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





"""
peticion:
{
  "id":"id de la peticion"
  "action":"aprobeAccountRequest",
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

class ApproveAccountRequest:

  req = Requests()
  users = Users()

  def handleAction(self, server, message):

    if message['action'] != 'approveAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])


    pid = message['id']
    reqId = message['reqId']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      reqs = self.req.listRequests(con)
      for r in reqs:
          if r['id'] == reqId:
              r2 = ObjectView(r)
              user = { 'dni':r2.dni, 'name':r2.name, 'lastname':r2.lastname }
              self.users.createUser(con,user)
              self.req.removeRequest(con,reqId)
              con.commit()


      response = {'id':pid, 'ok':'usuario creado correctamente'}
      server.sendMessage(json.dumps(response))

      event = {
        'type':'AccountRequestApprovedEvent',
        'data':reqId
      }
      self.events.broadcast(server,event)

      return True

    except psycopg2.DatabaseError, e:

        response = {'id':pid, 'error':''}
        server.sendMessage(json.dumps(response))

        if con:
            con.rollback()

    finally:
        if con:
            con.close()
