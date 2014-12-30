# -*- coding: utf-8 -*-
import json

"""
    Módulo que soporta el envío de eventos y mensajes hacia el lado cliente usando el websocket


    Los mensajes enviados al lado cliente son de la forma :

    {
        type: 'tipo de evento enviado'
        data: 'datos del mensaje (estos dependen del evento)'
    }

"""




class Events:


    def broadcast(self,server,msg):
        broadcast = json.dumps(msg)

        print "enviando datos de broadcast a los clientes : " + broadcast

        for c in server.server.connections.itervalues():
          c.sendMessage(broadcast)
