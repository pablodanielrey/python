# -*- coding: utf-8 -*-
import json
import psycopg2
import inject
from model.userPassword import UserPassword
from model.session import Session



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
 O "ok":""
 O "error":"mensaje de error"
}

"""
class Login:

  userPassword = inject.attr(UserPassword)
  session = inject.attr(Session)

  def handleAction(self, server, message):

    if message['action'] != 'login':
      return False

    user = message['user']
    passw = message['password']
    credentials = {
        'username':message['user'],
        'password':message['password']
    }

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      rdata = self.userPassword.findUserPassword(con,credentials)
      if rdata == None:
        response = {'id':message['id'], 'error':'autentificación denegada'}
        server.sendMessage(json.dumps(response))
        return True

      sid = self.session.create({'id':rdata['user_id']})
      response = {'id':message['id'], 'ok':'', 'session':sid}
      print json.dumps(response);
      server.sendMessage(json.dumps(response))
      return True

    except psycopg2.DatabaseError, e:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(json.dumps(response))

    except TypeError, e:
        print e

    except Error, e:
        print e

    finally:
        if con:
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

  def handleAction(self, server, message):

    if message['action'] != 'logout':
      return False

    session = message['session']

    print("logout %s", (session))

    ok = {'id':message['id'], 'ok':''}
    response = json.dumps(ok)

    print("response : " + response);

    server.sendMessage(response)

    return True
