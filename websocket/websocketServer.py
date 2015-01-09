
from Ws.SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import json
import datetime
from wexceptions import MalformedMessage
from model.profiles import AccessDenied



class NullData(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class NotImplemented(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__




class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)



class WebsocketServer(WebSocket):

  def setActions(self,actions):
    self.actions = actions

  def sendException(self,e):
      msg = {'type':'Exception','name':e.__class__.__name__}
      jmsg = json.dumps(msg, cls=DateTimeEncoder)
      self.sendMessage(jmsg)

  def sendError(self,msg,e):
      mmsg = {'id':msg['id'],'error':e.__class__.__name__}
      jmsg = json.dumps(mmsg, cls=DateTimeEncoder)
      self.sendMessage(jmsg)

  def handleMessage(self):
    try:
      if self.data is None:
        raise NullData()

      print 'C:' + self.data
      message = json.loads(str(self.data))

      if 'action' not in message:
        raise MalformedMessage()

      if 'id' not in message:
        raise MalformedMessage()

      try:
          managed = False
          for action in self.actions:
            managed = action.handleAction(self,message)
            if managed:
              break

      except AccessDenied as e:
          print e.__class__.__name__ + ' ' + str(e)
          self.sendError(message,e)
          managed = True

      except Exception as e:
          print e.__class__.__name__ + ' ' + str(e)
          self.sendError(message,e)
          raise e

      if not managed:
        raise NotImplemented()

    except Exception as e:
      print e.__class__.__name__ + ' ' + str(e)
      self.sendException(e)


  def sendMessage(self,msg):
      print 'R:' + str(msg)
      jmsg = json.dumps(msg,cls=DateTimeEncoder)
      print 'RJ' + jmsg
      super(WebsocketServer,self).sendMessage(jmsg)


  def handleConnected(self):
    print("connected : ",self.address)

  def handleClose(self):
    print("closed : ",self.address)
