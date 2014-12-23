# -*- coding: utf-8 -*-
import json

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
class LogoutAction:

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





