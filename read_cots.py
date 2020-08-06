import time
#from time import sleep,gmtime,strftime
from sys import version_info
import os
import uuid
#from socket import getfqdn
import socket 

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
print("read the Connect response")
print(takserver.read())  # read all the server CoT's, will send last + the connct

#print("Flush the server response")
#takserver.flush()  # flush the xmls the server sends
#time.sleep(3)

count = 1

#for i in range(10):
while True:
    print()

    print("wait for a server CoT- count = " +str(count))
    print(takserver.read(readtimeout=10))
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


