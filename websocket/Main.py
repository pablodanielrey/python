# -*- coding: utf-8 -*-
import signal, sys
import inject

from Ws.SimpleWebSocketServer import SimpleWebSocketServer
from GenericServer import GenericServer

from actions.chat import SendEventToClients
from actions.login import Login, Logout
from actions.requests import CreateAccountRequest, ListAccountRequests, ApproveAccountRequest
from actions.users import UpdateUser, FindUser, ListUsers, ListMails, PersistMail

from model.session import Session


def config_injector(binder):
    binder.bind(Session,Session())


if __name__ == '__main__':


  inject.configure(config_injector)

  ''' aca se definen las acciones a ser manejadas por el server '''

  actions = [
    SendEventToClients(),
    Login(), Logout(),
    CreateAccountRequest(), ListAccountRequests(), ApproveAccountRequest(),
    ListUsers(), UpdateUser(), FindUser(), ListMails(), PersistMail()
  ]


  ''' codigo de inicialización del servidor '''

  server = SimpleWebSocketServer('192.168.0.100',8001,GenericServer,actions)

  def close_sig_handler(signal,frame):
    server.close()
    sys.exit()

  signal.signal(signal.SIGINT,close_sig_handler)
  server.serveforever()
