# -*- coding: utf-8 -*-
import json, uuid, psycopg2
import inject
from model.users import Users
from model.events import Events

"""
    Modulo de acceso al manejo de usuarios
"""

"""
peticion:
{
    "id":"",
    "action":"listMails"
    "session":"sesion de usuario"
    "user_id":'id de usuario'
}

respuesta:
{
    "id":"id de la petición",
    "mails":[
        {
         "id":"",
         "user_id":"id de usuario",
         "email":"",
         "confirmed":true|false
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListMails:

  users = inject.attr(Users);

  def handleAction(self, server, message):

    if message['action'] != 'listMails':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      rdata = self.users.listMails(con, message['user_id'])
      response = {'id':message['id'], 'ok':'', 'mails': rdata}
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
    "id":"",
    "action":"persistMail",
    "session":"session de usuario",
    "mail": {
        "user_id":"id de la persona",
        "email":"email de la persona"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class PersistMail:

  users = inject.attr(Users)
  events = inject.attr(Events)

  def handleAction(self, server, message):

    if (message['action'] != 'persistMail'):
        return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')

      email = message['mail']
      if email == None:
          response = {'id':message['id'], 'error':''}
          server.sendMessage(json.dumps(response))
          return True


      user = self.users.findUser(con,email['user_id']);
      if user == None:
          response = {'id':message['id'], 'error':'usuario inválido'}
          server.sendMessage(json.dumps(response))
          return True


      self.users.createMail(con,email);
      con.commit()

      response = {'id':message['id'], 'ok':''}
      server.sendMessage(json.dumps(response))

      event = {
        'type':'UserUpdatedEvent',
        'data':user['id']
      }
      self.events.broadcast(server,event)


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
    "id":"",
    "action":"updateUser"
    "session":"sesion de usuario"
    "user":{
        "id":"id de usuario",
        "name":'nombre',
        "lastname":'apellido',
        "dni":"dni",
    }
}

respuesta:
{
    "id":"id de la petición",
    "ok":"",
    "error":""
}

"""

class UpdateUser:

  req = inject.attr(Users)
  events = inject.attr(Events)


  def handleAction(self, server, message):

    if (message['action'] != 'updateUser'):
        return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')

      user = message['user']
      if user == None:
          response = {'id':message['id'], 'error':''}
          server.sendMessage(json.dumps(response))
          return True


      self.req.updateUser(con,user);
      con.commit()

      response = {'id':message['id'], 'ok':''}
      server.sendMessage(json.dumps(response))

      event = {
        'type':'UserUpdatedEvent',
        'data':user['id']
      }
      self.events.broadcast(server,event)


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
    "id":"",
    "action":"findUser"
    "session":"sesion de usuario"
    "user":{
        "id":"id de usuario"
    }
}

respuesta:
{
    "id":"id de la petición",
    "user":[
        {
         "id":"",
         "dni":"",
         "name":"",
         "lastname":""
        }
      ],
    "ok":"",
    "error":""
}

"""

class FindUser:

  req = Users()


  def handleAction(self, server, message):

    if (message['action'] != 'findUser'):
        return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')

      if ((message['user'] == None) or (message['user']['id'] == None)):
          response = {'id':message['id'], 'error':''}
          server.sendMessage(json.dumps(response))
          return True

      id = message['user']['id']
      user = self.req.findUser(con,id)
      response = {'id':message['id'], 'ok':'', 'user': user}
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
    "id":"",
    "action":"listUsers"
    "session":"sesion de usuario"
}

respuesta:
{
    "id":"id de la petición",
    "users":[
        {
         "id":"",
         "dni":"",
         "name":"",
         "lastname":""
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListUsers:

  req = Users()

  def handleAction(self, server, message):

    if message['action'] != 'listUsers':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      rdata = self.req.listUsers(con)
      response = {'id':message['id'], 'ok':'', 'users': rdata}
      print json.dumps(response);
      server.sendMessage(json.dumps(response))

    except psycopg2.DatabaseError, e:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(json.dumps(response))

    finally:
        if con:
            con.close()

    return True
