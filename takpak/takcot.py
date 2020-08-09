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
            self.logging.debug("takserver connection closed")
        except:
            closereturn = 0
            self.logging.debug("Socket Close failed")
        return closereturn

    def send(self, cotdata, sleeptime=.075 ):
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

            except KeyboardInterrupt:
                self.logging.debug("Kbd Interrupt during read")
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

            if cot_xml.startswith("<?xml"):
                #print("Looks valid")
                #return cot_xml, frag
                return cot_xml, cots[1]
            else:
                # Must have had an incomplete cot fragment
                # Ignore the invalid CoT
                print("Not a valid CoT")
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


