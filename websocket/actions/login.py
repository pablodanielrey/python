# -*- coding: utf-8 -*-
import json
import psycopg2
import inject
from model.config import Config
from model.events import Events
from model.userPassword import UserPassword
from model.session import Session, SessionNotFound
from wexceptions import MalformedMessage


"""
        Modulo que contiene las clases de acceso a la funcionalidad de login/logout
"""




"""
peticion :

{
  "id":"id de la peticion"
  "action":"login",
  "user":"usuario",
  "password":"clave"
}

respuesta :

{
  "id":"id de la peticion"
  "session":"id de sesion a usar para la ejecución de futuras funciones",
  "user_id":'id del usuario logueado'
  "ok":""
  "error":"mensaje de error"
}

"""
class Login:

  userPassword = inject.attr(UserPassword)
  session = inject.attr(Session)
  config = inject.attr(Config)
  events = inject.attr(Events)

  def sendEvents(self,server,user_id):
      event = {
        'type':'UserLoggedInEvent',
        'data':user_id
      }
      self.events.broadcast(server,event)


  def handleAction(self, server, message):

    if message['action'] != 'login':
      return False

    user = message['user']
    passw = message['password']
    credentials = {
        'username':message['user'],
        'password':message['password']
    }

    con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
    try:
      rdata = self.userPassword.findUserPassword(con,credentials)
      if rdata == None:
        response = {'id':message['id'], 'error':'autentificación denegada'}
        server.sendMessage(json.dumps(response))
        return True

      sess = {
        self.config.USER_ID:rdata['user_id']
      }
      sid = self.session.create(sess)

      response = {'id':message['id'], 'ok':'', 'session':sid, 'user_id':rdata['user_id']}
      server.sendMessage(json.dumps(response))

      self.sendEvents(server,rdata['user_id'])

      ''' para debug '''
      print str(self.session)

      return True

    finally:
        con.close()





"""
peticion :

{
  "id":"id de la peticion"
  "action":"logout",
  "session":"sesion del usuario"
}

respuesta :

{
  "id":"id de la peticion"
 O "ok":""
 O "error":"mensaje de error"
}

"""
class Logout:

  session = inject.attr(Session)
  events = inject.attr(Events)
  config = inject.attr(Config)

  def sendEvents(self,server,user_id):
      event = {
        'type':'UserLoggedOutEvent',
        'data':user_id
      }
      self.events.broadcast(server,event)


  def handleAction(self, server, message):

    if message['action'] != 'logout':
      return False

    if 'session' not in message:
        raise MalformedMessage()

    uid = None
    sid = message['session']
    try:
        sess = self.session.findSession(sid)
        uid = sess[self.config.USER_ID]
        self.session.destroy(sid)
    except SessionNotFound as e:
        pass

    ok = {'id':message['id'], 'ok':''}
    response = json.dumps(ok)
    server.sendMessage(response)

    if uid:
        self.sendEvents(server,uid)

    ''' para debug '''
    print str(self.session)

    return True
