# -*- coding: utf-8 -*-
import json, uuid
import ActionUtils
import json

"""
peticion:
{
  "id":"id de la peticion"
  "action":"aprobeCreateRequest",
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


class AprobeCreateRequest:

  def handleAction(self, server, message):

    if message['action'] != 'aprobeCreateRequest':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    pid = message['id']
    reqId = message['reqId']
    
    response = {'id':pid, 'ok':'usuario creado correctamente'}
    server.sendMessage(json.dumps(response))

    return True





