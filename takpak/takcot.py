# takcot.py
__author__ = 'Alan Barrow <traveler@pinztrek.com>'
__copyright__ = 'Copyright 2020 Alan Barrow'
__license__ = 'GPL, Version 3+'
class takcot():
    """
    Connects, Sends and receives properly formed CoT's to TAK servers
    Tested on FTS, but should work on TAK
    """


    import os
    #from time import sleep,gmtime,strftime
    import time

    import logging
    import socket

    # Setup Logging
    LOGGERFORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(level=logging.DEBUG
        , format=LOGGERFORMAT
        , datefmt='%m/%d/%Y %I:%M:%S') 
    
    # Create a socket the methods can use
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open(self, ip_address, port=8087):
        self.logging.debug("Opening: " + ip_address + ":" + str(port))
        #self.logging.debug(self.sock)
        try:
            conn = self.sock.connect((ip_address, port))
            #self.logging.debug("Connect Return is:")
            #self.logging.debug(conn)
        except:
            self.logging.warning("Cannot connect to " + str(ip_address) + ":" + str(port))
            self.sock = 0
            exit()
        return self.sock
        
    def close(self):
        try:
            #closereturn = self.sock.shutdown(1)
            #time.sleep(0.2)
            closereturn = self.sock.close()
        except:
            closereturn = 0
            self.logging.debug("Socket Close failed")
        return closereturn

    def send(self, cotdata, sleeptime=0.075 ):
        #self.logging.debug(cotdata)
        sentdata=""
        try:
            sentdata = self.sock.send(cotdata)
            #self.logging.debug("sent")
        except:
            self.logging.warning("push_tcp: Send data failed")
            return 0
        # Now read what was sent
        #try:
        #    self.sock.settimeout(1)
        #    rcvdata = self.sock.recv(2048)
        #    self.logging.debug("pushTCP Rcv Data:" + str(rcvdata))
        #except:
        #    self.logging.warning("push_tcp: Rcv data failed")
        #    return 0
        # Set a minimum delay so the server does not get overrun    
        #self.time.sleep(self.sleeptime)  
        return sentdata

    # Get rid of any old messages, really should not be needed with unique UID's
    def flush(self):
        self.sock.settimeout(1)

        #response = 'start some reading'
        #Flush any pending server responses
        while True:
            #print("Read attempt: " + str(i))
            try:
                response = self.sock.recv(2048)
                #print("flushit response is:")
                #print(response)
                pass

            except:
                #print("flushit read empty")
                # Flushed, now return
                break

    def read(self, readattempts=5, readtimeout=1):
        self.sock.settimeout(readtimeout)

        response = ''
        for i in range(readattempts):
            #print("Read attempt: " + str(i))
            try:
                response = self.sock.recv(2048)
                #print("readit response is:")
                #print(response)
                return response

            except:
                #print("readit read empty")
                pass

        return response

