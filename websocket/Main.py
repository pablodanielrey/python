
from Ws.SimpleWebSocketServer import SimpleWebSocketServer
from GenericServer import GenericServer
from actions.LoginAction import LoginAction
from actions.LogoutAction import LogoutAction
from actions.CreateAccountRequestAction import CreateAccountRequestAction
from actions.ListAccountRequestsAction import ListAccountRequestsAction
from actions.AprobeRequest import AprobeRequest
from actions.SendEventToClientsAction import SendEventToClientsAction
import signal, sys

if __name__ == '__main__':

  ''' aca se definen las acciones a ser manejadas por el server '''

  login = LoginAction()
  logout = LogoutAction()
  createRequest = CreateAccountRequestAction()
  listRequests = ListAccountRequestsAction()
  aprobeRequests = AprobeRequest()
  sendEventToClients = SendEventToClientsAction()



  ''' codigo de inicialización del servidor '''

  server = SimpleWebSocketServer('',8001,GenericServer,[login,logout,createRequest,listRequests,aprobeRequests,sendEventToClients])

  def close_sig_handler(signal,frame):
    server.close()
    sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)
  server.serveforever()
