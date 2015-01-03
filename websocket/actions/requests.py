# -*- coding: utf-8 -*-
import json, uuid, psycopg2, inject
from model.requests import Requests
from model.users import Users
from model.objectView import ObjectView
from model.events import Events
from model.profiles import Profiles
from model.mail import Mail
from wexceptions import MalformedMessage

"""
    Modulo de acceso a la capa de las peticiones de cuentas.

"""


"""
peticion:
{
  "id":"id de la peticion"
  "action":"removeAccountRequest",
  "session":"id de session obtenido en el login",
  "reqId":"id del request a eliminar"
}

respuesta:
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

"""


class RemoveAccountRequest:

  req = inject.attr(Requests)
  events = inject.attr(Events)
  profiles = inject.attr(Profiles)

  def handleAction(self, server, message):

    if message['action'] != 'removeAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    if 'id' not in message:
        raise MalformedMessage()

    if 'reqId' not in message:
        raise MalformedMessage()

    pid = message['id']
    rid = message['reqId']

    con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
    try:
      self.req.removeRequest(con,rid)
      con.commit()

      response = {'id':pid, 'ok':'petición eliminada correctamente'}
      server.sendMessage(json.dumps(response))

      event = {
        'type':'AccountRequestRemovedEvent',
        'data': rid
      }
      self.events.broadcast(server,event)

      return True

    except psycopg2.DatabaseError as e:

        con.rollback()
        raise e

    finally:
        con.close()






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

    con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
    try:
      self.req.createRequest(con,data)
      con.commit()

      response = {'id':pid, 'ok':'petición creada correctamente'}
      server.sendMessage(json.dumps(response))

      event = {
        'type':'NewAccountRequestEvent',
        'data': data['id']
      }
      self.events.broadcast(server,event)

      return True

    finally:
        con.close()






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

  req = inject.attr(Requests)
  profiles = inject.attr(Profiles)

  def handleAction(self, server, message):

    if message['action'] != 'listAccountRequests':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
    try:
      rdata = self.req.listRequests(con)
      response = {'id':message['id'], 'ok':'', 'requests': rdata}
      server.sendMessage(json.dumps(response))
      return True

    finally:
        con.close()






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

eventos :

AccountRequestAprovedEvent
UserUpdatedEvent

"""

class ApproveAccountRequest:

  req = inject.attr(Requests)
  users = inject.attr(Users)
  profiles = inject.attr(Profiles)
  events = inject.attr(Events)
  mail = inject.attr(Mail)


  def sendEvents(self,server,req_id,user_id):
      event = {
        'type':'AccountRequestApprovedEvent',
        'data':req_id
      }
      self.events.broadcast(server,event)

      event = {
        'type':'UserUpdatedEvent',
        'data':user_id
      }
      self.events.broadcast(server,event)


  def sendNotificationMail(self,request):
      pass


  def handleAction(self, server, message):

    if message['action'] != 'approveAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN'])

    pid = message['id']
    reqId = message['reqId']

    con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
    try:
      req = self.req.findRequest(con,reqId)
      if (req == None):
          return True

      user = {
        'dni':req['dni'],
        'name':req['name'],
        'lastname':req['lastname']
      }
      user_id = self.users.createUser(con,user)
      self.users.createMail(con,{
            'user_id':user_id,
            'email':req['email']
      })
      self.req.removeRequest(con,reqId)

      con.commit()

      response = {'id':pid, 'ok':'usuario creado correctamente'}
      server.sendMessage(json.dumps(response))

      self.sendEvents(server,reqId,user_id)

      self.sendNotificationMail(req)

      return True

    except psycopg2.DatabaseError as e:
        con.rollback()
        raise e

    finally:
        con.close()
