import time
#from time import sleep,gmtime,strftime
from sys import version_info
import os
import uuid
#from socket import getfqdn
import socket 
import json
import logging
from  xml.dom.minidom import parseString
#import xml.dom.minidom 

import xml.etree.ElementTree as ET

# Bail if not python 3 or later
#if sys.version_info.major < 3:
if version_info.major < 3:
    print("Must use python 3 or later")
    exit()


#import takcot. Note this only works if you have installed the package
#   If you have not installed as a package, you may have to tune your imports
#   to be local to where your source is
from takpak.mkcot import mkcot
from takpak.takcot import takcot

# Setup Logging
LOGGERFORMAT = '%(asctime)s %(message)s'
logging.basicConfig(
    format=LOGGERFORMAT
    , datefmt='%m/%d/%Y %I:%M:%S')
logger = logging.getLogger(__name__)

# Select a logging level
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

# select a server, default to local
server = input('Server? local is default, "FTS" or "DISCORD" uses those public servers: ')
server = server.upper()

if server.startswith("F"):
    TAK_IP = os.getenv('TAK_IP', '204.48.30.216')
    TAK_PORT = int(os.getenv('TAK_PORT', '8087'))
    server = "FTS"
    logger.debug(server + " Server selected")

elif server.startswith("D"):
    TAK_IP = os.getenv('TAK_IP', '128.199.70.11')
    TAK_PORT = 48088
    server = "DISCORD"
    logger.debug(server + " Server selected")
else:
    # use the local server for default
    TAK_IP = '172.16.30.30'
    TAK_PORT = 8087
    server = "Local"
    logger.debug(server + " Server selected")


#open the users list
userfile = 'users.json'
try:
    f = open(userfile, "r+")
    try:
        users = json.load(f)
        logger.info("Initial Users loaded")
        logger.debug(users)
    except:
        logger.warning("users json load failed")
        users = []
    finally:
        f.close()
except:
    users = []
    logger.warning("Users file open failed, resetting")

#print()


#-----------------------------------------------------------------------------------------


# substantiate the class
try:
    takserver = takcot(logger=logger)
except:
    logger.error("takcot class failed")
    exit()

# Now open server
logger.debug("Opening TAK Server " + server + "----------------------------------------------------")
try:
    testsock = takserver.open(TAK_IP,TAK_PORT)
except:
    logger.error("takserver open failed")
    exit()

logger.debug("send a takserver connect")
try:
    takserver.flush()  # flush the xmls the server sends (should not be any)
except:
    logger.error("takserver flush failed")

connect_xml = mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")
#connect_xml = mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o",cot_platform="linux",cot_os="29")

my_xml = connect_xml.decode('utf-8')
my_xml = parseString(str(my_xml.replace("\n","")))
xml_pretty_str = my_xml.toprettyxml()

logger.debug("Connect XML is: " + xml_pretty_str)

# send the connect string, server does not echo
try:
    takserver.send(mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")) 
except:
    logger.error("takserver connect send failed")
    exit()


#print("Main read loop --------------------------------------------------------------------")
count = 1
frag = ""
while True:

    # Read a buff
    try:
        #logger.debug("reading ------------------------------------------------")
        cotresponse = takserver.readcot(readtimeout=1,frag=frag)

    except KeyboardInterrupt:
        logger.warning('Keyboard Interrupt- shutting down')
        takserver.close()
        raise

    except:
        logger.debug("readcot usercode exception")
        #continue        

    cot_xml = cotresponse[0]
    frag = cotresponse[1]

    #logger.debug("returned cot_xml= " + cot_xml)
    #logger.debug("returned frag= " + frag)

    if not cot_xml:
        time.sleep(0.1)
        #print("readcot returned No Data")
        continue

    # OK, we have a cot it appears
    logger.debug("CoT- " + str(count) + " --------------------------------------------------------------------")

    this_call=""
    this_team=""
    # Now try to parse the XML
    # Really need to turn this into mkcot methods
    try:

        tree = ET.fromstring(cot_xml)

        # Get the UID
        this_uid = tree.get("uid")

        try:
            detail_blk = tree.find("detail")
            contact_blk = detail_blk.find("contact")
            #print("contact.get callsign")
            this_call = contact_blk.get("callsign")
        except:
            #print("No callsign")
            this_call = "None"
        
        try:
            #detail_blk = tree.find("detail")
            group_blk = detail_blk.find("__group")
            #print("contact.get callsign")
            this_team = group_blk.get("name")
        except:
            #print("No team")
            this_team = "None"
       
        if this_call != "None": 
            user_new = True
            for user in users:
                #print(user)
                #print(user[0])
                if user[0] == this_call:
                    user_new = False
            
            if user_new:
                logger.info("New user " + this_call + " ")
                try:
                    user = [this_call,this_uid,this_team]
                    users.append(user)
                    #print(users)
                    #users_json = json.dumps(users)
                    #print(users_json)
                    try:
                        f = open(userfile, "w")
                        try:
                            json.dump(users,f)
                            f.close()
                            #print("New user " + this_call + " written to " + userfile)
                            logger.debug("New user written to " + userfile)
                        except:
                            logger.warning("json write failed")
                        finally:
                            #print("closing " + userfile)
                            f.close()
                    except:
                        logger.warning("File open failed- " + userfile)
                except:
                    logger.warning("Users append failed")
                #print("user " + this_call + " added " + str(len(users)))

        # OK, we have the basics
        if this_uid.endswith("-ping"):
            ping_uid = this_uid[:-5]
            # Now try to lookup the callsign of the ping if known
            ping_call = ""
            for user in users:
                if user[1] == ping_uid:
                    ping_call = user[0]
                    break
            logger.info("Ping: " + ping_call + " uid: " + this_uid)

        elif this_uid.startswith("Chat."):
            logger.info("Geochat: " + this_uid)

        else:
            logger.info("user: " + this_call + " uid: " + this_uid + " team: " + this_team)
        
        try:
            #print("Looking for recipients")
            #detail_blk = tree.find("detail")

            group_blk = detail_blk.find("__chat")
            #print("group_blk.get chatroom")

            this_recipient = group_blk.get("chatroom")
            this_sender = group_blk.get("senderCallsign")
            #print("Recip: " + this_recipient)
        except:
            #print("No chat")
            this_recipient = ""

        if this_recipient:
            #print("Looking for msg")
            #detail_blk = tree.find("detail")
            try:
                remarks_blk = detail_blk.find("remarks")
            except:
                logger.debug("No Remarks Block")

            try: 
                #this_to = remarks_blk.get("to")
                #print("this_to: " + this_to)
                #this_msg = remarks_blk.tail
                this_msg = remarks_blk.text
            except:
                logger.debug("No remarks msg")
                this_recipient = "None"
            logger.info("Sender: " + this_sender + " Recipient: " + this_recipient + " Msg: " + this_msg  )

        


    except:
        logger.debug("parse failed")
        pass

    my_xml = parseString(str(cot_xml.replace("\n","")))
    xml_pretty_str = my_xml.toprettyxml()

    logger.debug("Parsed CoT XML is: " + xml_pretty_str)
    #logger.debug("Parsed CoT XML is: " + cot_xml )

    
    time.sleep(0.1)
    count += 1
    if count > 5:
        # Send a keep-alive
        logger.debug("Keep alive sent -----------------------------------------")
        takserver.send(mkcot.mkcot(cot_ping=True, cot_type="t", cot_how="m-g")) 
        count = 1

# Always need to close out the connection
# good practice to include reading anything the server pushed
# to prevent broken pipe errors on the server

takserver.flush()  # flush the xmls the server sends

logger.info("Closing TAK Server")
takserver.close()


