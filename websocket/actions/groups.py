# -*- coding: utf-8 -*-
import psycopg2
import json, uuid, inject
from model.groups import Groups
from model.profiles import Profiles
from model.config import Config

"""
peticion:
{
    "id":"",
    "action":"listGroups"
    "session":"sesion de usuario"
}

respuesta:
{
    "id":"id de la petición",
    "groups":[
        {
         "id":"",
         "system_id":"",
         "name":"",
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListGroups:

  groups = inject.attr(Groups)
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  def handleAction(self, server, message):

    if message['action'] != 'listGroups':
      return False

    """ chequeo que exista la sesion, etc """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN','USER'])

    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      rdata = self.groups.listGroups(con)

      response = {'id':message['id'], 'ok':'', 'groups': rdata}
      server.sendMessage(response)
      return True

    finally:
        con.close()
