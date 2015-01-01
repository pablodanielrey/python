
from Ws.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import json

class WebsocketServer(WebSocket):

  def setActions(self,actions):
    self.actions = actions

  def ok(self, msg):
    return json.dumps({'ok':msg})

  def error(self, msg):
    return json.dumps({'error':msg})

  def handleMessage(self):
    try:
      if self.data is None:
        self.sendMessage(self.error('data == null'))
        return

      print("Loading %s", self.data)
      message = json.loads(str(self.data))

      if 'action' not in message:
        self.sendMessage(self.error('action not found in message'))
        return

      managed = False
      for action in self.actions:
        managed = action.handleAction(self,message)
        if managed:
          break

      if not managed:
        self.sendMessage(self.error('action not implemented'))

    except:
      self.sendMessage(self.error('exception parsing message'))


  def handleConnected(self):
    print("connected : ",self.address)

  def handleClose(self):
    print("closed : ",self.address)
