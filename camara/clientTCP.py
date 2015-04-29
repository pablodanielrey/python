# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example client. Run simpleserv.py first before running this.
"""

from twisted.internet import reactor, protocol


#  ///////////////////////////////////////////////////
# ////////////////RTP MJPEG //////////////////////////
#  ///////////////////////////////////////////////////

from twisted.internet.protocol import DatagramProtocol

class RTP_MJPEG_Client(DatagramProtocol):

    def __init__(self, config):
        self.config = config
        # Previous fragment sequence number
        self.prevSeq = -1
        self.lost_packet = 0

    def datagramReceived(self, datagram, address):
        print ("Datagram mjpeg client")



#  ////////////////////////////////////////////////
# ///////////////// RTCP //////////////////////////
#  ////////////////////////////////////////////////
class RTCP_Client(DatagramProtocol):

    # def __init__(self):
        # Object that deals with RTCP datagrams
        # self.rtcp = rtcp_datagram.RTCPDatagram()

    def datagramReceived(self, datagram, address):
        print ("rtcp client")
        # SSRC Report recieved
        # self.rtcp.Datagram = datagram
        # self.rtcp.parse()
        # Send back our Reciever Report
        # saying that everything is fine
        # RR = self.rtcp.generateRR()
        # self.transport.write(RR, address)


#  ////////////////////////////////////////////////
# ///////////////// RTSP //////////////////////////
#  ////////////////////////////////////////////////

# a client protocol

class RTSPClient(protocol.Protocol):

    def __init__(self):
        self.config = {}

    def connectionMade(self):
        self.session = 1
        # send OPTIONS request
        to_send = "OPTIONS rtsp://" + self.config['ip'] + ":554" + self.config['request'] + " RTSP/1.0\n"
        to_send += "CSeq: 1\n"
        to_send += "User-Agent: Python MJPEG Client"

        self.transport.write(to_send.encode("utf-8"))
        print (to_send)

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print ("Client received:", data)
        # self.transport.loseConnection()

    def connectionLost(self, reason):
        print ("connection lost")

class RTSPClientFactory(protocol.ClientFactory):

    def __init__(self, config):
        self.protocol = RTSPClient
        self.config = config

    def buildProtocol(self, addr):
        prot = protocol.ClientFactory.buildProtocol(self, addr)
        prot.config = self.config
        return prot

    def clientConnectionFailed(self, connector, reason):
        print ("Connection failed - goodbye!")
        # reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print ("Connection lost - goodbye!")
        # reactor.stop()


#  //////////////////////////////////////////////////////////////
#  ////////////////////////// MAIN //////////////////////////////
#  //////////////////////////////////////////////////////////////

def idMsg():
    print

# this connects the protocol to a server runing on port 8000
def main():
    config = {'request': '/video.mp4',
        #   'login': '',
          'password': 'admin',
          'ip': '163.10.56.40',
          'port': 554,
          'udp_port': 5354}

    f = RTSPClientFactory(config)

    reactor.listenUDP(config['udp_port'], RTP_MJPEG_Client(config))
    reactor.listenUDP(config['udp_port'] + 1, RTCP_Client()) # RTCP
    reactor.connectTCP(config["ip"], 554, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
