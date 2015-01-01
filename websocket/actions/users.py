# -*- coding: utf-8 -*-
import json, uuid, psycopg2, re
import inject
import hashlib
import smtplib
from email.mime.text import MIMEText

from model.users import Users
from model.events import Events

"""
    Modulo de acceso al manejo de usuarios
"""





"""
peticion:
{
    "id":"",
    "action":"confirmMail",
    "sub_action":"generate|confirm",
    "session":"session de usuario",
    "mail_id": "id del email a confirmar"
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class ConfirmMail:

  users = inject.attr(Users)
  events = inject.attr(Events)


  def sendEmail(self, url, hash, email):

      smtp_host = '163.10.17.115'
      smtp_user = 'campus'
      smtp_pass = 'supmac'
      From = 'detise@econo.unlp.edu.ar'
      To = email

      link = re.sub('\#.*$','#/confirmMail',url)

      msg = MIMEText('<html><head></head><body><a href="' + link + hash + '">click aqui para confirmar la cuenta</a></body></html>')
      msg['Subject'] = 'email de confirmación de la cuenta'
      msg['From'] = From
      msg['To'] = To

      s = smtplib.SMTP(smtp_host)
      s.login(smtp_user,smtp_pass)
      s.sendmail(From, [To], msg.as_string())
      s.quit()

      return True




  def generateConfirmation(self,con,mail,url):

      hash = hashlib.sha1(mail['id'] + mail['user_id']).hexdigest()
      mail['hash'] = hash
      self.users.updateMail(con,mail)

      ''' envío el mail '''
      self.sendEmail(url,hash,mail['email'])


  def confirm(self,con,mail):
      mail['confirmed'] = True
      self.users.updateMail(con,mail)


  def handleAction(self, server, message):

    if (message['action'] != 'confirmMail'):
        return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    if 'sub_action' not in message:
        response = {'id':message['id'], 'error':'formato de mensaje erroneo'}
        server.sendMessage(json.dumps(response))
        return True

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')

      if message['sub_action'] == 'generate':
          email = message['mail_id']
          if email == None:
              response = {'id':message['id'], 'error':''}
              server.sendMessage(json.dumps(response))
              return True

          mail = self.users.findMail(con,email);
          if mail == None:
              response = {'id':message['id'], 'error':'mail inxesistente'}
              server.sendMessage(json.dumps(response))
              return True

          self.generateConfirmation(con,mail,message['url'])
          response = {'id':message['id'], 'ok':'email de confirmación enviado'}
          server.sendMessage(json.dumps(response))

          con.commit()

          return True

      if message['sub_action'] == 'confirm':
          email = message['hash']
          if email == None:
              response = {'id':message['id'], 'error':''}
              server.sendMessage(json.dumps(response))
              return True

          mail = self.users.findMailByHash(con,email);
          if mail == None:
              response = {'id':message['id'], 'error':'mail inxesistente'}
              server.sendMessage(json.dumps(response))
              return True

          self.confirm(con,mail)

          response = {'id':message['id'], 'ok':''}
          server.sendMessage(json.dumps(response))

          event = {
            'type':'UserUpdatedEvent',
            'data':mail['user_id']
          }
          self.events.broadcast(server,event)

          con.commit()

          return True



      response = {'id':message['id'], 'error':'acción no definida'}
      server.sendMessage(json.dumps(response))
      return True

    except smtplib.SMTPRecipientsRefused, e:

        err = json.dumps(e.recipients)
        response = {'id':message['id'], 'error':err}
        print response
        server.sendMessage(json.dumps(response))

    except psycopg2.DatabaseError, e:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(json.dumps(response))

    except:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(json.dumps(response))


    finally:
        if con:
            con.close()



"""
peticion:
{
    "id":"",
    "action":"listMails"
    "session":"sesion de usuario"
    "user_id":'id de usuario'
}

respuesta:
{
    "id":"id de la petición",
    "mails":[
        {
         "id":"",
         "user_id":"id de usuario",
         "email":"",
         "confirmed":true|false
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListMails:

  users = inject.attr(Users);

  def handleAction(self, server, message):

    if message['action'] != 'listMails':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      rdata = self.users.listMails(con, message['user_id'])
      response = {'id':message['id'], 'ok':'', 'mails': rdata}
      print json.dumps(response);
      server.sendMessage(json.dumps(response))

    except psycopg2.DatabaseError, e:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(json.dumps(response))

    finally:
        if con:
            con.close()

    return True



"""
peticion:
{
    "id":"",
    "action":"persistMail",
    "session":"session de usuario",
    "mail": {
        "user_id":"id de la persona",
        "email":"email de la persona"
    }
}

respuesta:
{
    "id":"id de la peticion",
    "ok":"",
    "error":""
}

"""

class PersistMail:

  users = inject.attr(Users)
  events = inject.attr(Events)

  def handleAction(self, server, message):

    if (message['action'] != 'persistMail'):
        return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')

      email = message['mail']
      if email == None:
          response = {'id':message['id'], 'error':''}
          server.sendMessage(json.dumps(response))
          return True


      user = self.users.findUser(con,email['user_id']);
      if user == None:
          response = {'id':message['id'], 'error':'usuario inválido'}
          server.sendMessage(json.dumps(response))
          return True


      self.users.createMail(con,email);
      con.commit()

      response = {'id':message['id'], 'ok':''}
      server.sendMessage(json.dumps(response))

      event = {
        'type':'UserUpdatedEvent',
        'data':user['id']
      }
      self.events.broadcast(server,event)


    except psycopg2.DatabaseError, e:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(json.dumps(response))

    finally:
        if con:
            con.close()

    return True








"""
peticion:
{
    "id":"",
    "action":"updateUser"
    "session":"sesion de usuario"
    "user":{
        "id":"id de usuario",
        "name":'nombre',
        "lastname":'apellido',
        "dni":"dni",
    }
}

respuesta:
{
    "id":"id de la petición",
    "ok":"",
    "error":""
}

"""

class UpdateUser:

  req = inject.attr(Users)
  events = inject.attr(Events)


  def handleAction(self, server, message):

    if (message['action'] != 'updateUser'):
        return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')

      user = message['user']
      if user == None:
          response = {'id':message['id'], 'error':''}
          server.sendMessage(json.dumps(response))
          return True


      self.req.updateUser(con,user);
      con.commit()

      response = {'id':message['id'], 'ok':''}
      server.sendMessage(json.dumps(response))

      event = {
        'type':'UserUpdatedEvent',
        'data':user['id']
      }
      self.events.broadcast(server,event)


    except psycopg2.DatabaseError, e:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(json.dumps(response))

    finally:
        if con:
            con.close()

    return True



"""

peticion:
{
    "id":"",
    "action":"findUser"
    "session":"sesion de usuario"
    "user":{
        "id":"id de usuario"
    }
}

respuesta:
{
    "id":"id de la petición",
    "user":[
        {
         "id":"",
         "dni":"",
         "name":"",
         "lastname":""
        }
      ],
    "ok":"",
    "error":""
}

"""

class FindUser:

  req = inject.attr(Users)


  def handleAction(self, server, message):

    if (message['action'] != 'findUser'):
        return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')

      if ((message['user'] == None) or (message['user']['id'] == None)):
          response = {'id':message['id'], 'error':''}
          server.sendMessage(json.dumps(response))
          return True

      id = message['user']['id']
      user = self.req.findUser(con,id)
      response = {'id':message['id'], 'ok':'', 'user': user}
      print json.dumps(response);
      server.sendMessage(json.dumps(response))


    except psycopg2.DatabaseError, e:

      response = {'id':message['id'], 'error':''}
      server.sendMessage(json.dumps(response))

    finally:
      if con:
        con.close()

    return True



"""
peticion:
{
    "id":"",
    "action":"listUsers"
    "session":"sesion de usuario"
}

respuesta:
{
    "id":"id de la petición",
    "users":[
        {
         "id":"",
         "dni":"",
         "name":"",
         "lastname":""
        }
      ],
    "ok":"",
    "error":""
}

"""

class ListUsers:

  req = inject.attr(Users)

  def handleAction(self, server, message):

    if message['action'] != 'listUsers':
      return False

    """ chequeo que exista la sesion, etc """
    session = message['session']

    try:
      con = psycopg2.connect(host='127.0.0.1', dbname='orion', user='dcsys', password='dcsys')
      rdata = self.req.listUsers(con)
      response = {'id':message['id'], 'ok':'', 'users': rdata}
      print json.dumps(response);
      server.sendMessage(json.dumps(response))

    except psycopg2.DatabaseError, e:

        response = {'id':message['id'], 'error':''}
        server.sendMessage(json.dumps(response))

    finally:
        if con:
            con.close()

    return True
