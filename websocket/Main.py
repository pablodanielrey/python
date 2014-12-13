
from Ws.SimpleWebSocketServer import SimpleWebSocketServer
from GenericServer import GenericServer
from LoginAction import LoginAction
from CreateAccountRequestAction import CreateAccountRequestAction
import signal, sys

if __name__ == '__main__':

  login = LoginAction()
  createRequest = CreateAccountRequestAction()

  server = SimpleWebSocketServer('',8000,GenericServer,[login,createRequest])
 
  def close_sig_handler(signal,frame):
    server.close()
    sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)
  server.serveforever()
