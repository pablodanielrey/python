
import json, uuid
import ActionUtils

"""
peticion:
{
"id":"",
"action":"listCreateAccountRequests"
"session":"sesion de usuario"
}

respuesta:
{
"id":"id de la petición",
"list":[
    {
     "id":"",
     "dni":"",
     "name":"",
     "lastname":"",
     "mail":""
    }
  ],
 "ok":"",
 "error":""
}

"""

class ListCreateAccountRequestsAction:

  def handleAction(self, server, message):

    if message['action'] != 'listCreateAccountRequests':
      return False



    ''' a modo de ejemplo retorno algunas dummy '''


    msg = {'ok':'',
           'list':[
              {'id':str(uuid.uuid4()),'dni':'1','name':'nombre1','lastname':'apellido1','mail':'m@gmail.com'},
              {'id':str(uuid.uuid4()),'dni':'2','name':'nombre2','lastname':'apellido2','mail':'m2@gmail.com'}
             ]
           }

    server.sendMessage(json.dumps(msg))
    return True





