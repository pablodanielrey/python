
from Ws.SimpleWebSocketServer import SimpleWebSocketServer
from GenericServer import GenericServer
from actions.LoginAction import LoginAction
from actions.CreateAccountRequestAction import CreateAccountRequestAction
import signal, sys

if __name__ == '__main__':

  ''' aca se definen las acciones a ser manejadas por el server '''

  login = LoginAction()
  createRequest = CreateAccountRequestAction()



  ''' codigo de inicialización del servidor '''

  server = SimpleWebSocketServer('',8000,GenericServer,[login,createRequest])
 
  def close_sig_handler(signal,frame):
    server.close()
    sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)
  server.serveforever()
