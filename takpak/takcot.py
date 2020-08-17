# takcot.py
__author__ = 'Alan Barrow <traveler@pinztrek.com>'
__copyright__ = 'Copyright 2020 Alan Barrow'
__license__ = 'GPL, Version 3+'
import os
#from time import sleep,gmtime,strftime
import time

import logging
import socket

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class SocketError(Error):

    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class takcot():
    """
    Connects, Sends and receives properly formed CoT's to TAK servers
    Tested on FTS, but should work on TAK
    """



    def __init__(self, logger=None):
        # use existing logger
        self.logger = logger or logging.getLogger(__name__)

        self.logger.debug(__name__ + " self.logger logging started")

        self.sock = None
        
    def open(self, ip_address, port=8087):
        self.logger.debug(__name__ + " Opening: " + ip_address + ":" + str(port))
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.logger.debug(__name__ + " socket created")
        except:
            self.logger.error(__name__ + " socket create failed")
            exit()
        
        self.logger.debug(__name__ + " Opening Socket")
        try:
            conn = self.sock.connect((ip_address, port))
            #self.logger.debug("Connect Return is:")
            #self.logger.debug(conn)
        except:
            self.logger.error(__name__ + " Cannot connect to " + str(ip_address) + ":" + str(port))
            self.sock = None
        return self.sock
        
    def close(self):
        try:
            #closereturn = self.sock.shutdown(1)
            #time.sleep(0.2)
            closereturn = self.sock.close()
            self.logger.debug(__name__ + "takserver connection closed")
        except:
            closereturn = 0
            self.logger.warning(__name__ + " Socket Close failed")
        return closereturn

    def send(self, cotdata, sleeptime=.075 ):
        self.logger.debug(cotdata)
        try:
            self.logger.debug(__name__ + " Socket fileno: " + str(self.sock.fileno()))
            if self.sock.fileno() == -1:
                self.logger.error(__name__ + " Socket Closed")
                raise SocketError(__name__ + "Socket Closed")
        except:
            self.logger.error(__name__ +  " Could not get socket status")
            raise SocketError(__name__ + "could not get socket status")
        sentdata=""
        try:
            self.sock.settimeout(0.5) # 0 is non-blocking
            sentdata = self.sock.send(cotdata)
            if sentdata != len(cotdata):
                self.logger.error(__name__ +  " Socket Send mismatch " + str(sentdata) + " " +str(len(cotdata)))
                raise SocketError(__name__ + " Socket Send mismatch " + str(sentdata) + " " +str(len(cotdata)))
            #self.logger.debug("sent")

        except socket.timeout:
            self.logger.error(__name__ +  " Socket Timeout")
            raise SocketError(__name__ + "Socket Timeout")
            
        except:
            self.logger.warning(__name__ + " Send data failed")
            raise SocketError(__name__ + "Send Failed")
        # Now read what was sent
        #try:
        #    self.sock.settimeout(1)
        #    rcvdata = self.sock.recv(2048)
        #    self.logger.debug("pushTCP Rcv Data:" + str(rcvdata))
        #except:
        #    self.logger.warning("push_tcp: Rcv data failed")
        #    return 0
        # Set a minimum delay so the server does not get overrun    
        #self.time.sleep(self.sleeptime)  
        return sentdata

    # Get rid of any old messages, really should not be needed with unique UID's
    def flush(self, readtimeout=0.5):
        self.sock.settimeout(readtimeout)

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
        return 0 

    def read(self, readattempts=5, readtimeout=0.5):
        self.sock.settimeout(readtimeout)

        response = ''
        for i in range(readattempts):
            #print("Read attempt: " + str(i))
            try:
                response = self.sock.recv(2048)
                #print("readit response is:")
                #print(response)
                return response

            except KeyboardInterrupt:
                self.logger.debug("Kbd Interrupt during read")
                raise

            except:
                #print("readit read empty")
                pass

        return response

    def readcot(self, readtimeout=10, frag=""):
        # Read a buff
        #print("readcot passed frag= " + frag)
        #print("readtimeout= " + str(readtimeout))
        try:
            cotbuff = self.read(readtimeout=readtimeout,readattempts=1)
            #print("readcot successful read")
        except:
            # Nothing read in timeout
            print("Nothing read in timeout, but now process any frag")
            #return "",frag

        #print("cotbuff length is: " + str(len(cotbuff)))
        #print("raw cotbuff:")
        #print(cotbuff)

        # OK, we read something, now prepend the frag and clean it up
        if cotbuff:
            #cotbuff = bytes(frag,'utf-8') + cotbuff
            cotbuff = frag + cotbuff.decode('utf-8')
        else:
            #cotbuff = bytes(frag,'utf-8')
            cotbuff = frag
            #print("No Data")

        # from here out cotbuff is a string

        cotbuff=cotbuff.replace("\n","")

        #print("cleaned cotbuff is:")
        #print(cotbuff)
        #print(type(cotbuff))
        #print()

        #cots="nothing"
        count = 1

        #while len(cots)>1:
        #print("cots length is: " + str(len(cots)))
        try:
            # split the buff using the closing event tag
            #print("splitting cotbuff")
            cots=cotbuff.split("/event>",1)

        except:
            # really should never get here
            print("cotbuff split failed")


        if len(cots) > 1:
            # OK, we have a cot it appears
            # The first part should be an xml hopefully
            cot_xml=cots[0] + "/event>"

            #print("function cot_xml: " + cot_xml)

            # The 2nd part is a frag if at all
            frag=cots[1]

            #print("function frag: " + frag)

            # FTS is not always sending the XML block with FTS version 1.0
            # so accept one beginning with the event block as valid
            if cot_xml.startswith("<?xml") or cot_xml.startswith("<event"):
                #print("Looks valid")
                #return cot_xml, frag
                return cot_xml, cots[1]
            else:
                # Must have had an incomplete cot fragment
                # Ignore the invalid CoT
                self.logger.warning(__name__ + " Not a valid CoT")
                self.logger.warning(cot_xml)
                return "", frag

        else:
            #print("Incomplete readcot:")
            #print(cotbuff)
            #print()
            #print(cots)
            #print("cots length " + str(len(cots)))
            # read buff did not have a "/event" in it, no Cot yet 
            cot_xml=""
            return "", cots[0]

        print("readcot Should never get here")


