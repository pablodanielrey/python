# -*- coding: utf-8 -*-
import json

""" 
peticion :

{
  "id":"id de la peticion"
  "action":"sendEventToClients",
  "data":"datos del evento"
}

respuesta :

{
  "id":"id de la peticion"
 O "ok":""
 O "error":"mensaje de error"
}

"""
class SendEventToClientsAction:

  def handleAction(self, server, message):

    if message['action'] != 'sendEventToClients':
      return False
         
    etype = message['type']
    data = message['data']

    print("Enviando evento %s a los clientes : %s", etype, data)

    br = {'type':etype,'data':data}
    broadcast = json.dumps(br)
    print(broadcast);
    for c in server.server.connections.itervalues():
      c.sendMessage(broadcast)

    ok = {'id':message['id'], 'ok':''}
    response = json.dumps(ok)

    print("response : " + response);

    server.sendMessage(response)

    return True





