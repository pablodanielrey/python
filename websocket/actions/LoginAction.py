
import json

class LoginAction:

  def handleAction(self, server, message):

    if message['action'] != 'login':
      return False
         
    user = message['user']
    passw = message['password']

    print("login with : %s and pass : %s", (user, passw))

    ok = {'ok':'', 'session':'32r0932jewf2f2fjefc23r3ufcweich328f2hf2ifc'}
    server.sendMessage(json.dumps(ok))

    return True





