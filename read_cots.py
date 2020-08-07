import time
#from time import sleep,gmtime,strftime
from sys import version_info
import os
import uuid
#from socket import getfqdn
import socket 

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

#logging.basicConfig(level=logging.INFO) # level=10

# select a server, default to local
server = input('Server? local is default, "FTS" or "DISCORD" uses those public servers: ')
if server == "FTS":
    TAK_IP = os.getenv('TAK_IP', '204.48.30.216')
    TAK_PORT = int(os.getenv('TAK_PORT', '8087'))

elif server == "DISCORD":
    TAK_IP = os.getenv('TAK_IP', '128.199.70.11')
    TAK_PORT = 48088
else:
    # use the local server for default
    TAK_IP = '172.16.30.30'
    TAK_PORT = 8087

#-----------------------------------------------------------------------------------------


# substantiate the class
takserver = takcot()

# Now open server
print("Opening TAK Server")
testsock = takserver.open(TAK_IP,TAK_PORT)

#print("open return is:")
#print(testsock)


print()
print("send a connect")
takserver.flush()  # flush the xmls the server sends
#print(takserver.read())  # read all the server CoT's, will send last + the connct

connect_xml = mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")
print("Connect XML is:")
print(connect_xml)

# send the connect string, server does not echo
takserver.send(mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")) 
# send the connect string, server does not echo

#time.sleep(5)
#print("read the Connect response")
#print(takserver.read())  # read all the server CoT's, will send last + the connct

#print("Flush the server response")
#takserver.flush()  # flush the xmls the server sends
#time.sleep(3)

print("start --------------------------------------------------------------------")
count = 1
frag = ""
#for i in range(10):
while True:
    #print()

    #print("wait for a server CoT- count = " +str(count))
    #print(takserver.read(readtimeout=10))

    # Read a buff
    cotbuff = takserver.read(readtimeout=10)

    #print("cotbuff length is: " + str(len(cotbuff)))
    #print("raw cotbuff:")
    #print(cotbuff)

    if not cotbuff:
        time.sleep(0.1)
        print("No Data")
        continue
    
    # OK, we read something, now prepend the frag and clean it up
    cotbuff = bytes(frag,'utf-8') + cotbuff

    #print("cotbuff is:")
    #print(cotbuff)
    #print(type(cotbuff))
    try:
        cotbuff = cotbuff.decode('utf-8') # convert to a string
    except:
        print("cotbuff decode failed")
    #print("decoded cotbuff is:")
    #print(cotbuff)
    #print(type(cotbuff))

    cotbuff=cotbuff.replace("\n","")

    #print("cleaned cotbuff is:")
    #print(cotbuff)
    #print(type(cotbuff))
    #print()

    cots="nothing"
    count = 1

    while len(cots)>1:
        #print("cots length is: " + str(len(cots)))
        try:
            # split the buff using the closing event tag
            cots=cotbuff.split("/event>",1)

            # The first part should be an xml hopefully
            cot_xml=cots[0] + "/event>"

            # The 2nd part is a frag if at all
            frag=cots[1]
            #print("Frag XML is: |" + frag + "|")

            # OK, we have a cot it appears
            print(str(count) + " --------------------------------------------------------------------")

            # Now try to parse the XML
            try:

                tree = ET.fromstring(cot_xml)
                #print("ET dump")
                #ET.dump(tree)
                #print(tree.items())
                #print(tree.keys())
                #print("tree.get uid")
                #print(tree.get("uid"))
    
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

                # OK, we have the basics
                print(',["' + this_uid + '","' + this_call + '","' + this_team + '"]')
                
                try:
                    #print("Looking for recipients")
                    #detail_blk = tree.find("detail")
                    group_blk = detail_blk.find("__chat")
                    #print("group_blk.get chatroom")
                    this_recipient = group_blk.get("chatroom")
                    print("Recip: " + this_recipient)
                except:
                    #print("No chat")
                    this_recipient = ""

                if this_recipient:
                    print("Looking for msg")
                    #detail_blk = tree.find("detail")
                    try:
                        remarks_blk = detail_blk.find("remarks")
                    except:
                        print("No Remarks Block")
   
                    try: 
                        this_to = remarks_blk.get("to")
                        print("this_to: " + this_to)
                        #this_msg = remarks_blk.tail
                        this_msg = remarks_blk[0].tail
                    except:
                        print("No remarks msg")
                        this_recipient = "None"
                    print(',["' + this_recipient + '","' + this_msg + '"]')

                
                print()

                #root=tree.getroot()
                #print("Root: " + str(root))
                #print(root.tag)
                #for child in root:
                #    print(child.tag, child.attrib)
                #detail=parsed.detail
                #print("detail:")
                #print(detail)
                #lat=parsed.point.lat
                #print("lat:")
                #print(lat)

            except:
                print("parse failed")
                pass

            #print("CoT XML is: |" + cot_xml + "|")
            print("CoT XML is: " + cot_xml )

            # if the frag is "", then move along
            if not frag:
                break # end of the cotbuff

            cotbuff=frag
            count += 1
            
        except:
            #print("Split failed")
            cot_xml="" # no complete cot
            frag=cotbuff
            #print("remaining buff:")
            #print(cotbuff)
            #print("frag xml is:")
            #print(frag)
            break

        #print(str(count) + " --------------------------------------------------------------------")

    
    
    time.sleep(0.1)
    count += 1
    if count > 5:
        # Send a keep-alive
        print()
        print("Keep alive sent")
        takserver.send(mkcot.mkcot(cot_type="t", cot_how="h-g-i-g-o")) 
        count = 1

# Always need to close out the connection
# good practice to include reading anything the server pushed
# to prevent broken pipe errors on the server

#takserver.flush()  # flush the xmls the server sends

print("Closing TAK Server")
takserver.close()


