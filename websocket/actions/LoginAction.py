# -*- coding: utf-8 -*-
import json

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
class LoginAction:

  def handleAction(self, server, message):

    if message['action'] != 'login':
      return False
         
    user = message['user']
    passw = message['password']

    print("login with : %s and pass : %s", (user, passw))

    ok = {'id':message['id'], 'ok':'', 'session':'32r0932jewf2f2fjefc23r3ufcweich328f2hf2ifc'}
    response = json.dumps(ok)

    print("response : " + response);

    server.sendMessage(response)

    return True





