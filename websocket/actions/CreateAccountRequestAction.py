
import json, uuid
import ActionUtils
import json

"""
peticion:
{
  "id":"id de la peticion"
  "action":"createAccountRequest",
  "session":"id de session obtenido en el login"
  "dni":""
  "name":""
  "lastname":""
  "mail":""
  "reason":""
}

respuesta:  
{
  "id":"id de la peticion"
  O "ok":""
  O "error":""
}

"""


class CreateAccountRequestAction:

  def handleAction(self, server, message):

    if message['action'] != 'createAccountRequest':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    pid = message['id']
    dni = message['dni']
    name = message['name']
    lastname = message['lastname']
    mail = message['mail']
    reason = message["reason"]
    
    response = {'id':pid, 'ok':'petición creada correctamente'}
    server.sendMessage(json.dumps(response))

    return True





