
from Ws.SimpleWebSocketServer import SimpleWebSocketServer
from GenericServer import GenericServer
from actions.LoginAction import LoginAction
from actions.LogoutAction import LogoutAction
from actions.CreateAccountRequestAction import CreateAccountRequestAction
from actions.ListCreateAccountRequestsAction import ListCreateAccountRequestsAction
from actions.AprobeCreateRequest import AprobeCreateRequest
import signal, sys

if __name__ == '__main__':

  ''' aca se definen las acciones a ser manejadas por el server '''

  login = LoginAction()
  logout = LogoutAction()
  createRequest = CreateAccountRequestAction()
  listRequests = ListCreateAccountRequestsAction()
  aprobeRequests = AprobeCreateRequest()



  ''' codigo de inicialización del servidor '''

  server = SimpleWebSocketServer('',8001,GenericServer,[login,logout,createRequest,listRequests,aprobeRequests])
 
  def close_sig_handler(signal,frame):
    server.close()
    sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)
  server.serveforever()
