
import json, uuid
import ActionUtils

class CreateAccountRequestAction:

  def handleAction(self, server, message):

    if message['action'] != 'createAccountRequest':
      return False

    fields = ['dni','name','lastname','mail']
    ef = ActionUtils.checkRequiredFields(message,fields)
    if len(ef) > 0:
      server.sendMessage(server.error('Required fields ' + str(ef) + ' not found'))
      return True

    dni = message['dni']
    name = message['name']
    lastname = message['lastname']
    mail = message['mail']



    server.sendMessage(server.ok('request created with id : ' + str(uuid.uuid4())))
    return True





